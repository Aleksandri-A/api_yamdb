from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, signup, get_tokens_for_user

router = DefaultRouter()

app_name = 'users'
router.register(prefix='users', viewset=UserViewSet)
urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', get_tokens_for_user),
    path('', include(router.urls)),
]
