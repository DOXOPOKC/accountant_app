from django_q.tasks import async_task, fetch_group
from rest_framework import status
from rest_framework.parsers import (FileUploadParser, MultiPartParser)
from rest_framework.response import Response
from rest_framework.views import APIView

from bluebird.models import (Contragent, ContractNumberClass, DocumentsPackage,
                             OtherFile)
from bluebird.serializers import (ContragentShortSerializer,
                                  ContragentFullSerializer,
                                  TaskSerializer, PackageShortSerializer,
                                  PackageFullSerializer, OtherFileSerializer)
from bluebird.utils import (parse_from_file, get_data, get_object,
                            create_unique_id, calc_create_gen_async)


class ContragentsView(APIView):
    """ Вью для списка контрагентов """
    parser_class = [FileUploadParser, MultiPartParser]

    def get(self, request):
        conrtagents = Contragent.objects.all()
        serializer = ContragentShortSerializer(conrtagents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        file = request.FILES['file']
        if file:
            result = parse_from_file(file)
            group_id = create_unique_id()
            for data_element in result:
                if data_element['klass'] == 1:
                    contract_number = ContractNumberClass.create(new=True)
                    data_element['number_contract'] = contract_number.pk
                    serializer = ContragentFullSerializer(data=data_element)
                    if serializer.is_valid(True):
                        serializer.save()
                        async_task(get_data, int(serializer['id'].value),
                                   group=group_id)
                else:
                    continue  # TODO add another variants
            return Response(group_id, status=status.HTTP_201_CREATED)
        else:
            raise FileNotFoundError('NO FILE!')


class ContragentView(APIView):
    """ Вью для одного конкретного контрагента """
    def get(self, request, pk):
        obj = get_object(pk, Contragent)
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

            group_id = create_unique_id()
            async_task(calc_create_gen_async, contragent, pack,
                       group=group_id)
            return Response(group_id, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageView(APIView):
    """ Вью конкретного пакета """
    def get(self, request, pk, package_id):
        package = get_object(package_id, DocumentsPackage)
        serializer = PackageFullSerializer(package)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, package_id):
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def put(self, request, pk, package_id):
        package = get_object(package_id, DocumentsPackage)
        if package.is_active:
            contragent = package.contragent

            group_id = create_unique_id()
            async_task(calc_create_gen_async, contragent, package, True,
                       group=group_id)
            return Response(group_id, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, package_id):
        package = get_object(package_id, DocumentsPackage)
        package.is_active = False
        package.save(force_update=True)
        return Response(status=status.HTTP_200_OK)


class TasksView(APIView):
    """ Вью результата выполнения группы задач """
    def get(self, request, group_id):
        results = fetch_group(group_id, failures=True)
        serializer = TaskSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OtherFilesView(APIView):
    """ Вью списка прочих документов """
    def get(self, request, package_id):
        results = OtherFile.objects.filter(content_object__id=package_id)
        serializer = OtherFileSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, package_id, file_id):
        serializer = OtherFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OtherFileView(APIView):
    """ Вью конкретного документа из прочих """
    def get(self, request, file_id):
        result = get_object(file_id, OtherFile)
        serializer = OtherFileSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, file_id):
        result = get_object(file_id, OtherFile)
        serializer = OtherFileSerializer(result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, file_id):
        result = get_object(file_id, OtherFile)
        result.delete()
        return Response(status=status.HTTP_200_OK)
