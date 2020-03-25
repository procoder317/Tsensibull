"""Subscription serializer for business logic
"""
import json
import requests

from datetime import timedelta
from django.conf import settings
from rest_framework import serializers as slzs

from .models import TsSubscription
from tsusers.models import TsUser
from utils.common import request_choices


class TsSubscriptionSerializer(slzs.Serializer):
    """serializer for subscription
    """
    user_name = slzs.CharField()
    plan_id = slzs.ChoiceField(choices=tuple(plan for plan in settings.PLAN_TABLE))
    start_date = slzs.DateField()
    request_type = slzs.ChoiceField(choices=request_choices())
    date = slzs.DateField(required=False)

    def validate(self, data):
        ret = super().validate(data)
        if data["request_type"] == "GET":
            if not data.get("user_name"):
                raise slzs.ValidationError({"user_name": "This Field is required ."})
        return ret

    def _make_payment(self, validated_data, amount):
        """used to make the payment through the third party api
        """
        input_data = {
            "user_name": validated_data["user_name"],
            "payment_type": 'DEBIT' if amount > 0 else 'CREDIT',
            "amount": abs(amount)
        }
        try:
            response = requests.post(settings.PAYMENTS_URL, json=input_data)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                raise slzs.ValidationError("payment failed")
        except Exception:
            raise slzs.ValidationError("payment failed")

    def create(self, validated_data):
        """used to create a new subscription
        """
        current_plan = settings.PLAN_TABLE[validated_data['plan_id']]
        amount = current_plan["cost"]
        self.validated_data['amount'] = amount
        user = TsUser.objects.get(user_name=validated_data["user_name"])
        # used id intensionally for now instead of the createed_at field for now
        # needs to use -created_at for ordering
        subscriptions = TsSubscription.objects.filter(user=user).order_by('-id')[:2]

        # check for existing subscription
        if subscriptions:

            # trial can be used only once intially when you move from free plan only to trial
            # or do a direct trial plan
            if validated_data['plan_id'] == "TRIAL":
                trial_count = TsSubscription.objects.filter(user=user, plan_id="TRIAL").count()
                if trial_count == 1:
                    raise slzs.ValidationError("Plan already used once")

                check_list = [plan for plan in settings.PLAN_TABLE.keys() if plan not in ("FREE", "TRIAL")]
                for subscription in subscriptions:
                    if subscription.plan_id in check_list:
                        raise slzs.ValidationError("You can't downgrade to Trial")

            # for all other cases if equal or unequal one can update the subscription
            #  assumtions as per real world usage
            #  make a payment with the diff if current latest plan is still active
            if subscriptions[0].valid_till is None or subscriptions[0].valid_till >= validated_data["start_date"]:

                # dont allow same plan to be again reapplied as
                # this way user can reset and increase his validity without paying a thing
                # to avoid it we do this
                if subscriptions[0].plan_id == validated_data['plan_id']:
                    raise slzs.ValidationError("Plan already exists")

                prev_plan = settings.PLAN_TABLE[subscriptions[0].plan_id]
                amount = current_plan["cost"] - prev_plan["cost"]
                self.validated_data['amount'] = amount

        # do payment
        payment_response = None
        if amount != 0.0:
            payment_response = self._make_payment(validated_data, amount)
        # upgrade / downgrade plan
        inp_data = {
            "user": user,
            "plan_id": validated_data['plan_id'],
            "start_date": validated_data['start_date'],
        }
        if isinstance(payment_response, dict) and payment_response.get("payment_id") is not None:
            inp_data["payment_id"] = payment_response["payment_id"]
        if current_plan["validity"] > -1:
            inp_data["valid_till"] = validated_data['start_date'] + timedelta(days=current_plan["validity"] - 1)
        return TsSubscription.objects.create(**inp_data)

    def get_subscription_details(self):
        """used to get an existing subscription
        """
        if self.validated_data.get("user_name") and not self.validated_data.get("date"):
            return TsSubscription.objects.filter(
                user__user_name=self.validated_data["user_name"], valid_till__isnull=False)
        else:
            # used id intensionally for now instead of the createed_at field for now
            # needs to use -created_at for ordering
            subscription_obj = TsSubscription.objects.filter(
                user__user_name=self.validated_data["user_name"]).order_by("-id")[:1]
            if subscription_obj and (subscription_obj[0].valid_till is None or
                                     subscription_obj[0].valid_till >= self.validated_data["date"]):
                return subscription_obj

    def response(self, instances=None):
        """
        custom deserializer for providing custom information
        """
        if self.validated_data['request_type'] == "POST":
            return {
                "status": "SUCCESS",
                "amount": self.validated_data["amount"]
            }
        if self.validated_data['request_type'] == "GET":
            if not instances:
                raise slzs.ValidationError("No active subscriptions found")

            if self.validated_data.get("user_name") and not self.validated_data.get("date"):
                resp_list = []
                for instance in instances:
                    resp_list.append({
                        "plan_id": instance.plan_id,
                        "start_date": instance.start_date,
                        "valid_till": instance.valid_till})
                return resp_list
            else:
                return {
                    "plan_id": instances[0].plan_id,
                    "days_left": "Infinite" if instances[0].plan_id == "FREE" else (instances[0].valid_till - self.validated_data["date"]).days + 1
                }
