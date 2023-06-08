from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as rf
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Category, Genre, Review, Title

from .permissions import (IsAdminOnly,
                          IsAuthorAdminModeratorOrReadOnlyPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitlePatchSerializer, TitleSerializer,
                          TitleUnsaveSerializer)


class TitleFilter(rf.FilterSet):
    genre = rf.CharFilter(field_name='genre__slug', lookup_expr='exact')
    category = rf.CharFilter(field_name='category__slug', lookup_expr='exact')
    year = rf.NumberFilter(field_name='year', lookup_expr='exact')
    name = rf.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']


class TitleViewSet(viewsets.ModelViewSet):
    """Вью функция для произведений"""

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        if self.request.method == 'PATCH':
            return TitlePatchSerializer
        return TitleUnsaveSerializer

    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOnly,)
    filter_backends = (rf.DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    filterset_class = TitleFilter


class GenreViewSet(viewsets.ModelViewSet):
    """Вью функция для жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    """Вью функция для категорий"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOnly,)
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
