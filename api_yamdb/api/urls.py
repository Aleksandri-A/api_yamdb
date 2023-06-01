from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, basename='title')
router.register('posts', GenreViewSet, basename='genre')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
