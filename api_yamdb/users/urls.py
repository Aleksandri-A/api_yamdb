from rest_framework.routers import DefaultRouter
from django.urls import path, include
from users.views import UserViewSet
from . import views

router = DefaultRouter()

app_name = 'users'
router.register(prefix='users', viewset=UserViewSet)
urlpatterns = [
    path('auth/signup/', views.signup),
    path('auth/token/', views.get_tokens_for_user),
    path('', include(router.urls)),
]
