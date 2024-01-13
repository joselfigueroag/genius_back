from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "username": {"write_only": True},
        }

    def create(self, validated_data):
        email = validated_data["email"]
        user = User.objects.create(email=email)
        user.set_password(validated_data["password"])
        user.save()

        Token.objects.create(user=user)

        return user


class UserSerializer(serializers.BaseSerializer):
    def to_representation(self, user):
        user_repre = {
            "email": user.email,
            "token": user.auth_token.key if hasattr(user, "auth_token") else "",
        }

        return user_repre
