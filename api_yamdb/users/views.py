from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import filters
from rest_framework.decorators import action

from users.serializers import UserSerializer, SignupSerializer, TokenSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated, ])
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
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
    try:
        user = get_object_or_404(User, username=username)
    except IntegrityError:
        return Response(
            '...',
            status=status.HTTP_400_BAD_REQUEST
        )
    refresh = RefreshToken.for_user(user)
    data = {'token': str(refresh.access_token)}
    return Response(data, status=status.HTTP_200_OK)
