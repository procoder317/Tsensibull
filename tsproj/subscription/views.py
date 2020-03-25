from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from .serializer import TsSubscriptionSerializer


class TsSubscriptionView(APIView):
    def get(self, request, **kwargs):
        request = {"request_type": 'GET'}
        if kwargs.get("username"):
            request["user_name"] = kwargs.get("username")
        if kwargs.get("date"):
            request["date"] = kwargs.get("date")
        serialize = TsSubscriptionSerializer(data=request, partial=True)
        serialize.is_valid(raise_exception=True)
        try:
            out = serialize.get_subscription_details()
            return Response(serialize.response(out), status=status.HTTP_200_OK)
        except ValidationError:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

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
        except Exception:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
