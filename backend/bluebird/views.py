import datetime
import os, tempfile, zipfile
from copy import deepcopy

from django_q.tasks import (
    Task,
    async_task,
    fetch_group)
from rest_framework import \
    status
from rest_framework.parsers import (
    FileUploadParser,
    MultiPartParser)
from rest_framework.permissions import \
    IsAuthenticated
from rest_framework.response import \
    Response
from rest_framework.views import \
    APIView

from django.shortcuts import redirect
from wsgiref.util import FileWrapper

from bluebird.models import (
    ContractNumberClass,
    Contragent,
    DocumentsPackage,
    DocumentTypeModel,
    NormativeCategory,
    OtherFile,
    PackFile,
    SingleFile,
    OtherFile,
    Event,
    Commentary,
    State,
    SignUser,
    STRATEGIES, STRATEGIES_LIST, ZIP_FILES_ACTIONS)
from bluebird.serializers import (
    ContragentFullSerializer,
    ContragentShortSerializer,
    NormSerializer,
    OtherFileSerializer,
    PackageFullSerializer,
    PackageShortSerializer,
    SignUserSerializer,
    TaskSerializer, CommentarySerializer)
from bluebird.utils import (
    calc_create_gen_async,
    create_unique_id,
    get_data,
    get_object,
    parse_from_file)

from .snippets import \
    str_remove_app


class ContragentsView(APIView):
    """ Вью для списка контрагентов """
    parser_class = [FileUploadParser, MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_superuser and request.user.is_staff:
            conrtagents = STRATEGIES[
                'Все'
                ]().execute_list_strategy(request.user)
        elif request.user.is_staff and not request.user.is_superuser:
            conrtagents = STRATEGIES[
                'Все по отделу'
                ]().execute_list_strategy(request.user)
        elif not request.user.is_staff and not request.user.is_superuser:
            conrtagents = STRATEGIES[STRATEGIES_LIST[
                request.user.department.strategy
                ]]().execute_list_strategy(request.user)
        if not conrtagents:
            return Response(data='Нет прав доступа к элементу.',
                            status=status.HTTP_403_FORBIDDEN)
        serializer = ContragentShortSerializer(conrtagents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        file = request.FILES['file']
        if file:
            # Если фаил есть
            try:
                result = parse_from_file(file)
            except Exception:
                return Response('Структура файла не верна.\
                    Пожалуста используйте правильную форму.',
                    status=status.HTTP_400_BAD_REQUEST)
            if not result:
                # Если фаил есть но он "пустой"
                return Response('Выбраный фаил пуст или содержит информацию,\
                    не соотвествующую формату.',
                    status=status.HTTP_400_BAD_REQUEST)
            group_id = create_unique_id()
            for data_element in result:
                if data_element['klass'] == 1:
                    contract_number = ContractNumberClass.create(new=True)
                    data_element['number_contract'] = contract_number.pk
                    data_element['current_user'] = None  # request.user.id
                    serializer = ContragentFullSerializer(data=data_element)
                    if serializer.is_valid(True):
                        serializer.save()
                        async_task(get_data, int(serializer['id'].value),
                                   group=group_id)
                else:
                    continue  # TODO add another variants
            return Response(group_id, status=status.HTTP_201_CREATED)
        else:
            # Если файла нет
            return Response('В запросе не найден фаил.\
                Пожалуйста, выберите фаил.',
                status=status.HTTP_400_BAD_REQUEST)


class ContragentView(APIView):
    """ Вью для одного конкретного контрагента """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        if request.user.is_superuser and request.user.is_staff:
            obj = STRATEGIES[
                'Все'
                ]().execute_single_strategy(pk, request.user)
        elif request.user.is_staff and not request.user.is_superuser:
            obj = STRATEGIES[
                'Все по отделу'
                ]().execute_single_strategy(pk, request.user)
        elif not request.user.is_staff and not request.user.is_superuser:
            obj = STRATEGIES[STRATEGIES_LIST[
                request.user.department.strategy
                ]]().execute_single_strategy(pk, request.user)
        if not obj:
            return Response(data='Нет прав доступа к элементу.',
                            status=status.HTTP_403_FORBIDDEN)
        serializer = ContragentFullSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        obj = get_object(pk, Contragent)
        serializer = ContragentFullSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackagesView(APIView):
    """ Вью списка пакетов документов """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        packages = DocumentsPackage.objects.filter(contragent__pk=pk)
        serializer = PackageShortSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        if DocumentsPackage.objects.filter(contragent__pk=pk,
                                           is_active=True).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        contragent = Contragent.objects.get(pk=pk)
        serializer = PackageShortSerializer(data={'contragent': contragent.pk})
        if serializer.is_valid():
            serializer.save()
            pack = DocumentsPackage.objects.get(contragent__pk=pk,
                                                is_active=True)
            pack.initialize_sub_folders()
            pack.change_state_to(State.objects.filter(is_initial_state=True)[0])

            group_id = pack.name_uuid
            async_task(calc_create_gen_async, contragent, pack,
                       group=group_id)

            contragent.current_user = request.user
            # contragent.save()
            return Response(group_id, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageView(APIView):
    """ Вью конкретного пакета """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, package_id):
        package = get_object(package_id, DocumentsPackage)
        if package.package_state.is_permitted(request.user.department):
            serializer = PackageFullSerializer(package)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            Response(data="Нет прав доступа к элементу.",
                     status=status.HTTP_308_PERMANENT_REDIRECT)

    def post(self, request, pk, package_id):
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        #  add file addition here

        pack = get_object(package_id, DocumentsPackage)
        docs_pack = PackFile.objects.filter(object_id=pack.id)
        docs_single = SingleFile.objects.filter(object_id=pack.id)
        docs_other = OtherFile.objects.filter(object_id=pack.id)
        for doc in (docs_pack + docs_single + docs_other):
            archive.write(doc.file_path)

        #  add file addition here
        archive.close()
        wrapper = FileWrapper(temp)
        response = Response(data=wrapper, status=status.HTTP_200_OK,
                            content_type='application/zip')
        response['Content-Disposition'] = f'attachment;\
         filename={pack.name_uuid}.zip'
        response['Content-Length'] = temp.tell()
        temp.seek(0)
        return response

    def put(self, request, pk, package_id):
        package = get_object(package_id, DocumentsPackage)
        group_id = package.name_uuid
        if not Task.get_group_count(group_id):
            if package.is_active:
                contragent = package.contragent
                async_task(calc_create_gen_async, contragent, package, True,
                           group=group_id)
                return Response(group_id, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, package_id):
        package = get_object(package_id, DocumentsPackage)
        event_id = request.data.get('event', None)
        if not event_id:
            package.set_inactive()
            return Response(status=status.HTTP_200_OK)
        else:
            event = Event.objects.get(id=event_id)
            if event.from_state == package.package_state:
                package.change_state_to(event.to_state)
                # if not any([
                #     event.to_state.is_permitted(dept.id
                #         ) for dept in event.from_state.departments.all()]):
                if event.to_state.is_final_state:
                    package.set_inactive()
                if package.package_state.is_permitted(
                                                request.user.department):
                    return Response(status=status.HTTP_200_OK)
                return Response(data="Статус успешно сменен.",
                                status=status.HTTP_308_PERMANENT_REDIRECT)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TasksView(APIView):
    """ Вью результата выполнения группы задач """
    def get(self, request, group_id):
        results = fetch_group(group_id, failures=True)
        serializer = TaskSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUsersView(APIView):
    """ Вью пользователей имеющих право подписи """
    def get(self, request):
        results = SignUser.objects.all()
        serializer = SignUserSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NormsView(APIView):
    """ Вью нормативов """
    def get(self, request):
        results = NormativeCategory.objects.all()
        serializer = NormSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OtherFilesView(APIView):
    """ Вью списка прочих документов """
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request, pk, package_id):
        results = OtherFile.objects.filter(object_id=package_id)
        serializer = OtherFileSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, package_id):
        package = get_object(package_id, DocumentsPackage)
        file_obj = request.data['file']
        doc_type = DocumentTypeModel.objects.get(doc_type="Прочие")
        file_instance = OtherFile.objects.create(
            file_obj=file_obj,
            content_object=package,
            file_type=doc_type,
            creation_date=datetime.date.today(),
            file_name=file_obj.name
        )
        file_instance.save()
        file_instance.file_path = str_remove_app(file_instance.file_obj.path)
        return Response(file_instance.save(), status=status.HTTP_200_OK)


class OtherFileView(APIView):
    """ Вью конкретного документа из прочих """
    permission_classes = (IsAuthenticated,)
    parser_classes = (FileUploadParser,)

    def get(self, request, pk, package_id, file_id):
        result = get_object(file_id, OtherFile)
        serializer = OtherFileSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, package_id, file_id):
        result = get_object(file_id, OtherFile)
        serializer = OtherFileSerializer(result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, package_id, file_id):
        result = get_object(file_id, OtherFile)
        result.delete()
        return Response(status=status.HTTP_200_OK)


class CommentaryPackageView(APIView):
    """ Вью для CRUD комментариев """
    permission_classes = (IsAuthenticated,)

    def get(self, request, package_id):
        comments = Commentary.objects.filter(package__id=package_id)
        serializer = CommentarySerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, package_id):
        package = get_object(package_id, DocumentsPackage)
        comment = package.commentary.create(
            user=request.user,
            commentary_text=request.data.get('commentary_text')
        )
        serializer = CommentarySerializer(data=comment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentaryFileView(APIView):
    """ Вью для CRUD комментариев """
    # permission_classes = (IsAuthenticated,)

    def get(self, request, package_id, file_id):
        comments = Commentary.objects.filter(file__id=package_id)
        serializer = CommentarySerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, package_id, file_id):
        other_file = get_object(package_id, OtherFile)
        comment = other_file.commentary.create(
            user=request.user,
            commentary_text=request.data.get('commentary_text')
        )
        serializer = CommentarySerializer(data=comment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
