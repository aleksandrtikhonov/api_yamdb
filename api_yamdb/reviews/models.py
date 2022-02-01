from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_ROLES = [
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(
        max_length=9,
        choices=USER_ROLES,
    )
    bio = models.TextField()
