"""Subscription serializer for business logic
"""
import json
import requests

from datetime import timedelta
from django.db.models import Q
from django.conf import settings
from rest_framework import serializers as slzs

from tsusers.models import TsUser
from .models import TsSubscription
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
        subscriptions = TsSubscription.objects.filter(user=user).order_by('-created_at')[:1]

        # check for existing subscription
        if subscriptions:

            # trial can be used only once
            trial_count = TsSubscription.objects.filter(user=user, plan_id="TRIAL").count()
            if validated_data['plan_id'] == "TRIAL" and trial_count == 1:
                raise slzs.ValidationError("Plan already used once")

            # as free plan is already with unlimited validity
            if subscriptions[0].plan_id == validated_data['plan_id'] and validated_data['plan_id'] == "FREE":
                raise slzs.ValidationError("Plan already exists")

            # for all other cases if equal or unequal one can update the subscription
            #  assumtions as per real world usage
            prev_plan = settings.PLAN_TABLE[subscriptions[0].plan_id]
            amount = current_plan["cost"] - prev_plan["cost"]

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
        """used to get an existing user
        """
        if self.validated_data.get("user_name") and not self.validated_data.get("date"):
            return TsSubscription.objects.filter(
                user__user_name=self.validated_data["user_name"], valid_till__isnull=False)
        else:
            return TsSubscription.objects.filter(
                Q(user__user_name=self.validated_data["user_name"], valid_till__gte=self.validated_data["date"]) |
                Q(user__user_name=self.validated_data["user_name"], valid_till__isnull=True)
            ).order_by("-created_at")[:1]

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
            if len(instances) > 1:
                resp_list = []
                for instance in instances:
                    resp_list.append({
                        "plan_id": instance.plan_id,
                        "start_date": instance.start_date,
                        "valid_till": instance.valid_till})
                return resp_list
            if len(instances) == 1:
                return {
                    "plan_id": instances[0].plan_id,
                    "days_left": "Infinite" if instances[0].plan_id == "FREE" else (instances[0].valid_till - self.validated_data["date"]).days + 1
                }
