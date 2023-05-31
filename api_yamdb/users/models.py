from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=254,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Confirm(models.Model):
    confirmation_code = models.CharField(max_length=400)
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='confirmation_code'
    )
