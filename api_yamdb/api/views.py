from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from reviews.models import Title, Genre, Category

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено.')
    #     super(PostViewSet, self).perform_update(serializer)

    # def perform_destroy(self, instance):
    #     if instance.author != self.request.user:
    #         raise PermissionDenied('Удаление чужого контента запрещено.')
    #     super(PostViewSet, self).perform_destroy(instance)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

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
