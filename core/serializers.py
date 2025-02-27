from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['style'] = {"input_type": 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class CreateUserSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User  # Импортируем из from core.models import User
        fields = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat")

    def validate(self, attrs: dict):
        if attrs["password"]:  # обязательное поле поэтому квадратные скобки, не через get != attrs["password_repeat"]:
            raise ValidationError(
                "Password must match")  # Импортируем из from rest_framework.exceptions import ValidationError
        return attrs

    def create(self, validated_data: dict):
        del validated_data["password_repeat"]  # удаление
        validated_data["password"] = make_password(validated_data["password"])  # шифровка пароля
        return super().create(validated_data)
