from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title, Genre, Category

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


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


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """Вью функция для жанров"""
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вью функция для категорий"""
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     post_id = self.kwargs.get('post_id')
    #     post = get_object_or_404(Post, pk=post_id)
    #     return post.comments.all()

    # def perform_create(self, serializer):
    #     post_id = self.kwargs.get('post_id')
    #     post = get_object_or_404(Post, pk=post_id)
    #     serializer.save(author=self.request.user, post=post)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого коммента запрещено.')
    #     super(CommentViewSet, self).perform_update(serializer)

    # def perform_destroy(self, instance):
    #     if instance.author != self.request.user:
    #         raise PermissionDenied('Удаление чужого коммента запрещено.')
    #     super(CommentViewSet, self).perform_destroy(instance)
