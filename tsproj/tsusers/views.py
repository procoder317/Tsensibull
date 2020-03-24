from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from utils.common import request_to_dict
from .serialzer import TsUserSerializer


class TsUserView(APIView):
    def get(self, request, **kwargs):
        request = request_to_dict(request.GET)
        request["user_name"] = kwargs.get("username")
        request["request_type"] = "GET"
        serializer = TsUserSerializer(data=request)
        serializer.is_valid(raise_exception=True)
        try:
            out = serializer.get_user()
            return Response(serializer.response(out), status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=500)

    # def post(self, request, **kwargs):
    #     return Response({"msg": "working"}, status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        request = request.data
        request["user_name"] = kwargs.get("username")
        request["request_type"] = "PUT"
        serializer = TsUserSerializer(data=request)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(None)
        except Exception as err:
            return Response({'error': str(err)}, status=500)

    # def delete(self, request, **kwargs):
    #     return Response({"msg": "working"}, status=status.HTTP_200_OK)
