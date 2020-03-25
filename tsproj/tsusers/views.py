from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serialzer import TsUserSerializer


class TsUserView(APIView):
    def get(self, request, **kwargs):
        request = {}
        request["user_name"] = kwargs.get("username")
        serializer = TsUserSerializer(data=request)
        serializer.is_valid(raise_exception=True)
        try:
            out = serializer.get_user()
            return Response(serializer.response(out), status=status.HTTP_200_OK)
        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        request = request.data
        request["user_name"] = kwargs.get("username")
        serializer = TsUserSerializer(data=request)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(None)
        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
