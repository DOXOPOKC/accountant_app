from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserShortSerializer


class UserView(APIView):
    def get(self, request):
        serializer = UserShortSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
