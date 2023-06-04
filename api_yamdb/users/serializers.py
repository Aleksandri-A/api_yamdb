from rest_framework import serializers

from django.core.exceptions import ValidationError

from users.models import User, Confirm, ROLE


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.RegexField(
    #     required=True,
    #     regex=r'^[\w.@+-]+\Z',
    #     max_length=150)
    # email = serializers.EmailField(
    #     required=True,
    #     allow_blank=False,
    #     trim_whitespace=True,
    #     max_length=254
    # )
    # bio = serializers.CharField(required=False, allow_blank=True)
    # first_name = serializers.CharField(
    #     max_length=150,
    #     required=False,
    #     allow_blank=True
    # )
    # last_name = serializers.CharField(
    #     max_length=150,
    #     required=False,
    #     allow_blank=True
    # )
    # role = serializers.ChoiceField(choices=ROLE)

    def validate_role(self, value):
        if (
            self.context['request'].user.role == 'admin'
            or self.context['request'].user.is_superuser
        ):
            return value
        return 'user'

    # def create(self, validated_data):

    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         bio=validated_data['bio'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #         role=validated_data['role']
    #     )
    #     return user

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class SignupSerializer(serializers.ModelSerializer):
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
        return value

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+\Z',
        max_length=150
    )
    confirmation_code = serializers. CharField(
        max_length=400,
        required=True,
    )

    class Meta:
        model = Confirm
        fields = ('username', 'confirmation_code')
