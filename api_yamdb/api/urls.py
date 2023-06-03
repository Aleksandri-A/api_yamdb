from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, basename='title')
router.register('genres', GenreViewSet, basename='genre')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path(
        'v1/categories/<slug:slug>/',
        CategoryViewSet.as_view({'delete': 'destroy'}),
        name='category-detail'
    ),
    path(
        'v1/genres/<slug:slug>/',
        GenreViewSet.as_view({'delete': 'destroy'}),
        name='genre-detail'
    ),
    path('v1/', include(router.urls)),
]
