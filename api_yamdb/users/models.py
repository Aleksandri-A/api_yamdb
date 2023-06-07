from django.contrib.auth.models import AbstractUser
from django.db import models


CUSTOMUSER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE = (
    (CUSTOMUSER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)


class User(AbstractUser):
    """Модель для юзера."""
    email = models.EmailField(unique=True, max_length=254,)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=255, choices=ROLE, default=CUSTOMUSER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def str(self):
        return self.username


class Confirm(models.Model):
    """Модель для кода подтверждения."""
    confirmation_code = models.CharField(max_length=400)
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )
