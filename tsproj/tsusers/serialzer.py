"""Users serialzer for the project
"""
from rest_framework import serializers as slzs

from .models import TsUser


class TsUserSerializer(slzs.Serializer):
    """serializer for users
    """
    user_name = slzs.CharField()

    def create(self, validated_data):
        """used to create a new user
        """
        return TsUser.objects.create(user_name=validated_data["user_name"])

    def get_user(self):
        """used to get an existing user
        """
        return TsUser.objects.get(user_name=self.validated_data["user_name"])

    def response(self, instance):
        """
        custom deserializer for providing custom information
        """
        return {
            "user_name": instance.user_name,
            "created_at": instance.created_at.__str__().split(".")[0]
        }
