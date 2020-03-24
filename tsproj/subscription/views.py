from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .serializer import TsSubscriptionSerializer


class TsSubscriptionView(APIView):
    def get(self, request, **kwargs):
        return Response({"msg": "working"}, status=status.HTTP_200_OK)

    def post(self, request, **kwargs):
        request = request.data
        request["request_type"] = 'POST'
        serialize = TsSubscriptionSerializer(data=request)
        serialize.is_valid(raise_exception=True)
        try:
            out = serialize.save()
            return Response(serialize.response(out), status=status.HTTP_200_OK)
        except ValidationError:
            return Response(
                {"status": "FAILURE", "amount": serialize.validated_data['amount']},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({'error': str(err)}, status=500)

    # def put(self, request, **kwargs):
    #     return Response({"msg": "working"}, status=status.HTTP_200_OK)

    # def delete(self, request, **kwargs):
    #     return Response({"msg": "working"}, status=status.HTTP_200_OK)
