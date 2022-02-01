import datetime as dt

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


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


def current_year():
    """
    Получаем текущий год.
    """
    return dt.date.today().year


def max_value_current_year(value):
    """
    Подставляем в валидатор текущий год,
    для валидации максимального значения поля.
    """
    return MaxValueValidator(current_year())(value)


class Title(models.Model):
    """
    Произведение.
    Например: название фильма, книги, песни и т.д.
    """
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=50,
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выхода',
        validators=[
            MinValueValidator(1000),
            max_value_current_year
        ]
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title'
    )

    def __str__(self):
        return self.name

