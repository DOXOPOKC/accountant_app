from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import UserShortSerializer


class UserView(APIView):

    def get(self, request):
        user = request.user or None
        serializer = UserShortSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
