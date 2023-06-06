from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.pagination import (LimitOffsetPagination,)
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Confirm, User
from users.permissions import IsAdminOnly
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вью функция для юзеров"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated, ])
    def me(self, request):
        """Фунция для получения и изменения данных своей учетной записи."""
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                context={'request': request},
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=400)
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signup(request):
    """Функция регистрации нового пользователя."""
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    try:
        user, created = User.objects.get_or_create(
            username=username, email=email
        )
    except IntegrityError:
        return Response(
            'Проверьте правильность Email',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)
    Confirm.objects.create(
        username=user, confirmation_code=confirmation_code
    )
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
    """Функция получения токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code != (
        Confirm.objects.get(username=user).confirmation_code
    ):
        return Response(
            'Введенный код не верный',
            status=status.HTTP_400_BAD_REQUEST
        )

    refresh = RefreshToken.for_user(user)
    data = {'token': str(refresh.access_token)}
    return Response(data, status=status.HTTP_200_OK)
