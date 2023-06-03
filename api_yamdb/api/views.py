from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import (PageNumberPagination,
                                       LimitOffsetPagination)
from rest_framework.permissions import (AllowAny, IsAdminUser,
                                        IsAuthenticatedOrReadOnly)

from reviews.models import Category, Genre, Title, Review, Title

from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          TitleUnsaveSerializer, CommentSerializer,
                          ReviewSerializer)
from .permissions import (IsAuthorAdminModeratorOrReadOnlyPermission, )


class TitleViewSet(viewsets.ModelViewSet):
    """Вью функция для произведений"""
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre', 'category', 'name', 'year')
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        return TitleUnsaveSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Вью функция для жанров"""
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    """Вью функция для категорий"""
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
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
