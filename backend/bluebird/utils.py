import json
import os
import uuid
from typing import List

import jinja2
import openpyxl
import pdfkit
import requests
from django.http import Http404
from django.template.loader import render_to_string
from django_q.tasks import async_task, fetch, result
from docxtpl import DocxTemplate


from bluebird.dadata import (Result_response_from_suggestion,
                             suggestions_response_from_dict)
from bluebird.models import (
    KLASS_TYPES,
    ActFile,
    ActUniqueNumber,
    Contragent,
    CountFactFile,
    CountFactUniqueNumber,
    CountFile,
    CountUniqueNumber,
    DocumentsPackage)
from bluebird.serializers import ContragentFullSerializer
from bluebird.templatetags.template_extra_filters import (gent_case_filter,
                                                          pretty_date_filter)

from blackbird.views import calculate


MIN_INNN_LEN = 10
MAX_INN_LEN = 12

TOKEN = os.environ.get('DADATA_TOKEN', '')
URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party'


def parse_from_file(xlsx_file):
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


def get_dadata_data(contragent_inn: int) -> dict:
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "Authorization": f"Token {TOKEN}"}
    data = {"query": contragent_inn}
    r = requests.post(
        URL,
        data=json.dumps(data),
        headers=headers,
        timeout=(3.0, 5.0),
    )
    return r.json()


def get_data(id: int):
    contragent = get_object(id, Contragent)
    data = get_dadata_data(contragent.inn)
    sug_d = suggestions_response_from_dict(data)
    if sug_d:
        if len(sug_d.suggestions):
            for d in sug_d.suggestions:
                is_result = d.data.state.status == 'ACTIVE'
                if is_result:
                    result = Result_response_from_suggestion(d)
                    serializer = ContragentFullSerializer(contragent,
                                                          data=result.data)
                    if serializer.is_valid():
                        serializer.save()
                        return {'inn': contragent.inn, 'status': "OK"}
            return {'inn': contragent.inn, 'status': "Not OK",
                    'errors': serializer.errors}
        else:
            return {'inn': contragent.inn,
                    'status': "0 length suggestion, something wrong."}
    else:
        return {'inn': contragent.inn,
                'status': "No suggestions. Check, DADATA is availiable?"}


def generate_documents(data: List, package: DocumentsPackage,
                       recreate: bool = False):
    """ Функция пакетной генерации документов."""
    package.contragent.create_package_and_folder()
    package.initialize_sub_folders()
    generate_contract(package)
    for d in data:

        generate_act(d, package, recreate)
        generate_count(d, package, recreate)

        generate_count_fact(d, package, recreate)


def generate_act(data: dict, package: DocumentsPackage,
                 recreate: bool = False):
    """ Функция генерации Акта """
    data['consumer'] = package.contragent
    curr_date = data['curr_date']
    if recreate:
        # Если пересоздаем акты
        acts = package.act_files.filter(creation_date=curr_date)
        if len(acts):
            # Если длинна результата не 0. Т.е. мы нашли акт на нужную дату.
            act = acts[0]
            unique_num = act.act_unique_number
            file_path = str_add_app(act.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            act.delete()
        else:
            # Если длинна результата 0. Т.е. актов нет. Например мы
            # выставили новую дату, на которую нет актов.
            unique_num = ActUniqueNumber.create()
    else:
        # Если мы создаем акт с нуля.
        unique_num = ActUniqueNumber.create()
    tmp_name = unique_num.number.replace('/', '-')
    file_name = f'Акт №{tmp_name} от {curr_date}.pdf'
    file_path = os.path.join(ActFile.get_files_path(package), file_name)
    data['uniq_num_id'] = unique_num
    text = render_to_string('act.html', context=data)
    generate_document(text, file_path)
    act = ActFile.objects.create(file_name=file_name,
                                 file_path=str_remove_app(file_path),
                                 content_object=package,
                                 creation_date=curr_date,
                                 act_unique_number=unique_num)
    return act


def generate_count(data: dict, package: DocumentsPackage,
                   recreate: bool = False):
    """ Функция генерации счета на оплату """
    data['consumer'] = package.contragent
    curr_date = data['curr_date']
    if recreate:
        # Если пересоздаем счета
        counts = package.count_files.filter(creation_date=curr_date)
        if len(counts):
            # Если длинна результата не 0. Т.е. мы нашли счет на нужную дату.
            count = counts[0]
            unique_num = count.count_unique_number
            file_path = str_add_app(count.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            count.delete()
        else:
            unique_num = CountUniqueNumber.create()
    else:
        # Если мы создаем счет с нуля.
        unique_num = CountUniqueNumber.create()
    tmp_name = unique_num.number.replace('/', '-')
    file_name = f'Счет №{tmp_name} от {curr_date}.pdf'
    file_path = os.path.join(CountFile.get_files_path(package), file_name)
    data['uniq_num_id'] = unique_num
    text = render_to_string('count.html', context=data)
    generate_document(text, file_path)
    count = CountFile.objects.create(file_name=file_name,
                                     file_path=str_remove_app(file_path),
                                     content_object=package,
                                     creation_date=curr_date,
                                     count_unique_number=unique_num)
    return count


def generate_count_fact(data: dict, package: DocumentsPackage,
                        recreate: bool = False):
    """ Функция генерации счета фактуры """
    data['consumer'] = package.contragent
    curr_date = data['curr_date']
    if recreate:
        # Если пересоздаем счета фактуры
        counts_f = package.count_fact_files.filter(creation_date=curr_date)
        if len(counts_f):
            # Если длинна результата не 0. Т.е. мы нашли счет фактуру на
            # нужную дату.
            count_f = counts_f[0]
            unique_num = count_f.count_fact_unique_number
            file_path = str_add_app(count_f.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            count_f.delete()
        else:
            unique_num = CountFactUniqueNumber.create()
    else:
        # Если мы создаем счет фактуру с нуля.
        unique_num = CountFactUniqueNumber.create()
    tmp_name = unique_num.number.replace('/', '-')
    file_name = f'Счет фактура №{tmp_name} от {curr_date}.pdf'
    file_path = os.path.join(CountFactFile.get_files_path(package), file_name)
    data['uniq_num_id'] = unique_num
    text = render_to_string('count_fact.html', context=data)
    options = {'orientation': 'Landscape',
               'page-size': 'A4',
               'margin-top': '0.75in',
               'margin-right': '0.75in',
               'margin-bottom': '0.75in',
               'margin-left': '0.75in'}
    generate_document(text, file_path, options=options)
    count_fact = CountFactFile.objects.create(
        file_name=file_name,
        file_path=str_remove_app(file_path),
        content_object=package,
        creation_date=curr_date,
        count_fact_unique_number=unique_num)
    return count_fact


def generate_contract(package: DocumentsPackage):
    """ Функция генерации контракта """
    doc = DocxTemplate('templates/docx/ul.docx')
    jinja_env = jinja2.Environment()
    jinja_env.filters['gent_case_filter'] = gent_case_filter
    jinja_env.filters['pretty_date_filter'] = pretty_date_filter
    data = {'consumer': package.contragent, }
    doc.render(data, jinja_env)
    tmp_name = str(package.contragent.number_contract).replace('/', '-')
    tmp_path = os.path.join(
        package.get_save_path(),
        f'Договор №{tmp_name}.docx')
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    doc.save(tmp_path)
    if os.path.isfile(tmp_path):
        package.contract = str_remove_app(tmp_path)
        package.save()


def generate_document(text: str, name: str, **kwargs):
    """ Функция генерации  PDF документа из заданного HTML текста """
    pdfkit.from_string(text, name, **kwargs)


def create_unique_id():
    """ Функция генерации уникального uuid """
    return str(uuid.uuid4())


def str_remove_app(string: str):
    return string.replace('/app', '')


def str_add_app(string: str):
    return string.replace('/media/', '/app/media/')


def calc_create_gen_async(contragent, pack, recreate: bool = False):
    calc_func = async_task(calculate, contragent.contract_accept_date,
                           contragent.current_date, contragent.stat_value,
                           contragent.norm_value)
    res = fetch(calc_func, wait=-1)
    gen_func = async_task(generate_documents, result(calc_func),
                          pack, recreate)
    is_gen = fetch(gen_func, wait=-1)
    return [res.success, is_gen.success]
