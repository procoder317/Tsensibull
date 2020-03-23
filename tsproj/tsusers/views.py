from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class TsUserView(APIView):
    def get(self, request, **kwargs):
        print(kwargs)
        return Response({"msg": "working"}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        print(kwargs)
        return Response({"msg": "working"}, status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        return Response({"msg": "working"}, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        return Response({"msg": "working"}, status=status.HTTP_200_OK)
