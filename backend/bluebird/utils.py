import json
import os
import uuid
from typing import List
import aiohttp
import datetime
import shutil

import jinja2
import openpyxl
import pdfkit
from asgiref.sync import async_to_sync
from django.http import Http404
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django_q.tasks import async_task, Task
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm


from bluebird.dadata import (result_response_from_suggestion,
                             suggestions_response_from_dict)
from bluebird.models import (
    KLASS_TYPES,
    DOC_TYPE,
    Contragent,
    PackFile,
    SyncUniqueNumber,
    PackFilesTemplate,
    DocumentsPackage,
    TemplateModel,
    DocumentTypeModel,
    SingleFilesTemplate,
    SingleFile)
from bluebird.serializers import ContragentFullSerializer
from bluebird.templatetags.template_extra_filters import (
    gent_case_filter,
    pretty_date_filter,
    datv_case_filter,
    cap_first,
    literal, proper_date_filter, remove_zero_at_end, sum_imp)

from blackbird.views import calculate, round_hafz

from .snippets import str_add_app, str_remove_app


MIN_INNN_LEN = 10
MAX_INN_LEN = 12

TOKEN = os.environ.get('DADATA_TOKEN', '')
URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party'


def parse_from_file(xlsx_file):
    """ Функция получения данных из экселя """
    xl = openpyxl.load_workbook(xlsx_file)
    sheet = xl.worksheets[0]
    results = []
    for row in sheet.iter_rows(min_row=3, max_row=42, min_col=2, max_col=5,
                               values_only=True):
        a, b, c, d = row
        # print('|', a, '|', b, '|', c, '|', d, '|')
        if a is not None:
            if MIN_INNN_LEN > len(str(a)) or len(str(a)) > MAX_INN_LEN:
                raise Exception(('200', 'Inn is wrong.'))
            else:
                if d != '' and 0 < d < len(KLASS_TYPES):
                    klass = KLASS_TYPES[d][0]
                else:
                    klass = 0
                tmp_obj = {
                    'inn': int(a),
                    'physical_address': b,
                    'excell_name': c,
                    'klass': klass
                }
                results.append(tmp_obj)
        else:
            continue
    return results


def get_object(pk, klass):
    try:
        return klass.objects.get(pk=pk)
    except klass.DoesNotExist:
        raise Http404


async def get_dadata_data(contragent_inn: int):
    """ Функция получения данных из ДаДаты """
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "Authorization": f"Token {TOKEN}"}
    data = {"query": contragent_inn}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            URL,
            data=json.dumps(data),
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=10*60)
        ) as resp:
            resp.raise_for_status()
            return await resp.json()


def get_data(id: int):
    """ Функция обработки данных из ДаДаты """
    contragent = get_object(id, Contragent)
    data = async_to_sync(get_dadata_data, True)(contragent.inn)
    # print(data)
    sug_d = suggestions_response_from_dict(data)
    if sug_d:
        if len(sug_d.suggestions):
            for d in sug_d.suggestions:
                is_result = d.data.state.status == 'ACTIVE'
                if is_result:
                    res = result_response_from_suggestion(d)
                    serializer = ContragentFullSerializer(contragent,
                                                          data=res)
                    if serializer.is_valid():
                        serializer.save()
                        return {'inn': contragent.inn, 'status': "OK"}
            return {'inn': contragent.inn, 'status': "Not OK",
                    'errors': 'Contragent not active.'}
        else:
            return {'inn': contragent.inn,
                    'status': "0 length suggestion, something wrong."}
    else:
        return {'inn': contragent.inn,
                'status': "No suggestions. Check, DADATA is availiable?"}


def generate_documents(data: dict, package: DocumentsPackage,
                       recreate: bool = False):
    """ Функция пакетной генерации документов."""
    package.contragent.create_package_and_folder()  # Создаем папку контрагента
    package.initialize_sub_folders()  # Создаем подпапки пакета
    total = round_hafz(count_total(data), 2)  # Считаем Итого.

    generate_single_files(data, package, total, recreate)

    generate_pack_doc(data, package, recreate)

    package.contragent.debt = total
    package.contragent.save()


def generate_pack_doc(data_list, package: DocumentsPackage,
                      recreate: bool = False):
    contragent = package.contragent

    try:
        # Находим запись шаблона со списком подпакетов.
        pack_template = PackFilesTemplate.objects.get(
            contagent_type=contragent.klass)
    except ObjectDoesNotExist:
        return

    # Находим экземпляры класса входящие в пакет.
    docs = PackFile.objects.filter(object_id=package.id)

    # Получаем список всех подпакетов.
    # И создаем словарь с экземплярами классов.
    tmp_template_doc_types_list = pack_template.documents.all()
    tmp_templ_dict = dict()
    for tmpl in tmp_template_doc_types_list:
        tmp_templ_dict[str(tmpl)] = list(docs.filter(file_type=tmpl))

    # Удаляем папки с файлами.
    delete_folders(package)

    if len(docs):  # Смотрим есть ли уже экземпляры класса.
        if recreate:  # Перегенерируем пакет?
            # Пакет перегенерируется. Экземпляры есть.

            # Находим экземпляры класса не входящие в перечень шаблонов.
            removed_docs = docs.exclude(
                file_type__in=tmp_template_doc_types_list)
            # Удаляем найденные записи.
            delete_models(removed_docs)
            for data in data_list:
                data['consumer'] = contragent
                data['sign_user_document'] = (
                    DOC_TYPE[contragent.signed_user.document][1])
                curr_date = data['curr_date']
                for doc_type in tmp_template_doc_types_list:
                    # Берем конкретную запись на дату и тип.
                    doc_list = docs.filter(creation_date=curr_date,
                                           file_type=doc_type)

                    # Если такая запись найдена продолжаем работать с ней.
                    if len(doc_list):
                        doc = doc_list[0]
                        template = get_template(doc_type, package)
                        if not template:
                            return None
                        # Если запись в словаре, то:
                        if doc in tmp_templ_dict[str(doc_type)]:

                            # Делаем если модель файла нормальная.
                            # Т.е. экземпляр без пути и имени нормальным не
                            # считается.
                            if doc.file_path and doc.file_name:

                                # Формируем путь из экземпляра.
                                file_path = str_add_app(doc.file_path)

                            else:
                                file_name = f'{doc_type.doc_type.title()} \
 №{doc.unique_number} от {data["curr_date"]}.pdf'.replace('/', '-')
                                file_path = os.path.join(
                                    doc.get_files_path(package),
                                    file_name)
                                doc.file_name = file_name
                                doc.file_path = str_remove_app(file_path)
                                doc.save(force_update=True)
                            # Инициализируем подпапки.
                            doc.get_files_path(package)

                            # Удаляем экземпляр из массива в словаре.
                            tmp_templ_dict[str(doc_type)].remove(doc)

                            # Создаем фаил.
                            create_files(data, template, file_path)
                            continue
                    # Создаем запись по переданным данным.
                    # Либо такого файла не найдено, что значит мы работаем с
                    # новой датой, либо экземпляры были удалены.
                    unique_number = SyncUniqueNumber.objects.create()
                    create_models(data, package, doc_type, unique_number)

            # Если после удаления найденых записей, еще остаются записи в
            # словаре, значит из шаблона были удалены подпакеты. И именно их
            # теперь необходимо удалить.
            for v in tmp_templ_dict.values():
                if len(v):
                    for item in v:
                        if item:
                            item.delete()
            return
        else:
            # Пакет создается с 0, но при этом есть экземпляры.
            # Такое вряд ли возможно, но на всякий случай удалим эти
            # экземпляры.
            delete_models(docs)
    # Здесь мы окажемся в 3х случаях:
    # - если мы с 0 создаем пакет;
    # - если создаем с 0 но при этом есть записи в базе с екземплярами класса
    # PackFile;
    #  - если пересоздаем, но екземпляров найдено не было.
    for data in data_list:
        data['consumer'] = contragent
        data['sign_user_document'] = (
                    DOC_TYPE[contragent.signed_user.document][1])
        unique_number = SyncUniqueNumber.objects.create()
        for doc_type in tmp_template_doc_types_list:
            create_models(data, package, doc_type, unique_number)


def create_models(data: dict, package: DocumentsPackage,
                  file_type: DocumentTypeModel,
                  unique_number: SyncUniqueNumber):
    """ Функция создания экземпляра модели PackFile по шаблону.
    На вход принимает:
    data - словарь с данными на определенную дату.
    package - пакет.
    file_type - тип генерируемого документа.
    """
    template = get_template(file_type, package)
    if not template:
        return None
    file_obj = PackFile.objects.create(
        content_object=package,
        creation_date=data['curr_date'],
        unique_number=unique_number,
        file_type=file_type)
    file_name = f'{file_type.doc_type.title()} \
 №{unique_number} от {data["curr_date"]}.pdf'.replace('/', '-')
    file_path = os.path.join(file_obj.get_files_path(package), file_name)

    create_files(data, template, file_path)
    file_obj.file_name = file_name
    file_obj.file_path = str_remove_app(file_path)
    file_obj.save(force_update=True)


def delete_folders(package: DocumentsPackage):
    """Функция удаления папок в указанном пакете.
    Удаляет все папки кроме папки "прочие". """
    dir_path = package.get_save_path()
    with os.scandir(dir_path) as it:
        for entry in it:
            if entry.is_dir() and not entry.name.startswith('прочие'):
                shutil.rmtree(entry.path, True)


def delete_models(docs):
    """ Функия удаления моделей. На вход получает список с экземплярами
    объектов."""
    for doc in docs:
        doc.delete()


def create_files(data: dict, template: TemplateModel, file_path: str):
    """ Фунция создания файлов.
    На вход получает:
    data - словарь с данными.
    template - экземпляр шаблона генерации.
    file_path - путь сохранения итогового документа в виде строки.
    """
    if os.path.isfile(template.template_path):
        text = render_to_string(template.template_path, context=data)
        generate_document(text, file_path)
    else:
        raise ObjectDoesNotExist('Template path does not exist.')


def generate_document(text: str, name: str, **kwargs):
    """ Функция генерации  PDF документа из заданного HTML текста """
    pdfkit.from_string(text, name, **kwargs)


def generate_single_files(data: dict, package: DocumentsPackage, total: float,
                          recreate: bool = False):
    try:
        document_types = SingleFilesTemplate.objects.get(
            contagent_type=package.contragent.klass)
        doc_types = document_types.documents.all()
        for document_type in doc_types:
            generate_docx_file(data, package, total, document_type, recreate)

        res = SingleFile.objects.filter(object_id=package.id).exclude(
            file_type__in=doc_types)
        for r in res:
            r.delete()
    except ObjectDoesNotExist:
        return Http404


def generate_docx_file(data: dict, package: DocumentsPackage, total: float,
                       document_type_obj: DocumentTypeModel,
                       recreate: bool = False):
    template = get_template(document_type_obj, package)
    if not template:
        return None
    doc = DocxTemplate(template.template_path)

    jinja_env = jinja2.Environment()
    jinja_env.filters['datv_case_filter'] = datv_case_filter
    jinja_env.filters['gent_case_filter'] = gent_case_filter
    jinja_env.filters['pretty_date_filter'] = pretty_date_filter
    jinja_env.filters['capfirst'] = cap_first
    jinja_env.filters['literal'] = literal
    jinja_env.filters['remove_zero_at_end'] = remove_zero_at_end
    jinja_env.filters['proper_date_filter'] = proper_date_filter
    jinja_env.filters['sum_imp'] = sum_imp
    context = {'data': data, 'consumer': package.contragent, 'total': total}
    if package.contragent.signed_user.sign:
        context['sign'] = InlineImage(doc, package.contragent.signed_user.sign,
                                      width=Mm(27))
    doc.render(context, jinja_env)
    tmp_name = str(package.contragent.number_contract).replace('/', '-')
    file_name = f'{str(document_type_obj)} ({tmp_name}).docx'
    tmp_path = os.path.join(
        package.get_save_path(),
        file_name)

    res = SingleFile.objects.filter(object_id=package.id,
                                    file_type=document_type_obj.id)
    if not len(res):
        SingleFile.objects.create(
                file_name=file_name,
                file_path=str_remove_app(tmp_path),
                content_object=package,
                creation_date=datetime.date.today(),
                file_type=document_type_obj)
    else:
        if recreate and os.path.isfile(tmp_path):
            os.remove(tmp_path)

    doc.save(tmp_path)
    return None


def create_unique_id():
    """ Функция генерации уникального uuid """
    return str(uuid.uuid4())


def count_total(data: dict):
    res = 0.0
    for data_piece in data:
        res += float(data_piece['summ_tax_precise'])
    return res


def calc_create_gen_async(contragent, pack, recreate: bool = False):
    try:
        async_task(calculate, contragent.contract_accept_date,
                   contragent.current_date, contragent.stat_value,
                   contragent.norm_value, pack, recreate,
                   hook=gen_async, group=pack.name_uuid)
    except AttributeError:
        raise Http404


def gen_async(task):
    if task.success:
        async_task(generate_documents, task.result, task.args[4], task.args[5],
                   hook=del_after_exec, group=task.group)
    else:
        del_after_exec(task)
        raise Http404


def del_after_exec(task):
    Task.delete_group(task.group)


def get_template(doc_type: DocumentTypeModel, package: DocumentsPackage):
    try:
        template = TemplateModel.objects.get(
            city=package.contragent.signed_user.city,
            contragent_type=package.contragent.klass,
            document_type=doc_type.id
            )
        return template
    except ObjectDoesNotExist:
        return Http404
