from rest_framework import serializers

from django.core.exceptions import ValidationError

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        return user

    class Meta:
        model = User
        fields = ("username", "email")


class SignupSerializer(serializers.Serializer):
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+\Z',
        max_length=150)
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        max_length=254
    )


def validate_username(self, value):
    username = value.lower()
    if username == 'me':
        raise ValidationError(
            'Username "me" не может быть создан, придумайте другое имя.'
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+\Z',
        max_length=150
    )
    confirmation_code = serializers. CharField(
        max_length=400,
        required=True,
    )
