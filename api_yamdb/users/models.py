from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=254,)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=255, choices=ROLE, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def str(self):
        return self.username


class Confirm(models.Model):
    confirmation_code = models.CharField(max_length=400)
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )
