from django.shortcuts import get_object_or_404
from django_filters import rest_framework as rf
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from rest_framework.pagination import (LimitOffsetPagination,)
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Confirm, User, CUSTOMUSER

from reviews.models import Category, Genre, Review, Title

from .permissions import (IsAdminOnly,
                          IsAuthorAdminModeratorOrReadOnlyPermission)
from .serializers import (SignupSerializer, TokenSerializer, UserSerializer,
                          CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleUnsaveSerializer)


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
                serializer.save(role=CUSTOMUSER)
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


class TitleFilter(rf.FilterSet):
    genre = rf.CharFilter(field_name='genre__slug', lookup_expr='exact')
    category = rf.CharFilter(field_name='category__slug', lookup_expr='exact')
    year = rf.NumberFilter(field_name='year', lookup_expr='exact')
    name = rf.CharFilter(field_name='name', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']


class TitleViewSet(viewsets.ModelViewSet):
    """Вью функция для произведений"""
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminOnly()]

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    filter_backends = (rf.DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleUnsaveSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Вью функция для жанров"""
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminOnly()]

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    """Вью функция для категорий"""
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminOnly()]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorAdminModeratorOrReadOnlyPermission,
        IsAuthenticatedOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user, title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorAdminModeratorOrReadOnlyPermission,
        IsAuthenticatedOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user, review=review
        )
