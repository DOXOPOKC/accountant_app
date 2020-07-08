from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from bluebird.models import DocumentsPackage, State, Contragent


class JournalView(APIView):
    def get(self, request, package_id):
        try:
            pack = DocumentsPackage.objects.get(pk=package_id)
            
        except ObjectDoesNotExist:
            return Response("Такого пакета не существует",
                            status=status.HTTP_404_NOT_FOUND)


class ReportView(APIView):
    def get(self, request, report_id):
        pass
