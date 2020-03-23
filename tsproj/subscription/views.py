from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TsSubscriptionView(APIView):
    def get(self, request, **kwargs):
        return Response({"msg": "working"}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        return Response({"msg": "working"}, status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        return Response({"msg": "working"}, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        return Response({"msg": "working"}, status=status.HTTP_200_OK)
