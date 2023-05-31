from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from users.serializers import UserSerializer, SignupSerializer, TokenSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    try:
        user = User.objects.create(
            username=username, email=email
        )
    except IntegrityError:
        return Response(
            'Проверьте правильность Email',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)
    print(confirmation_code)
    send_mail(
        subject='...',
        message=confirmation_code,
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def get_tokens_for_user(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    refresh = RefreshToken.for_user(username, confirmation_code)
    return {
        'token': str(refresh.access_token),
    }
