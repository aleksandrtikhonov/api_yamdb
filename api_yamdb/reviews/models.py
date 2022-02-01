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


class Category(models.Model):
    """
    Категория(тип) произведения.
    Например: фильм, книга, музыка и т.д.
    """
    name = models.CharField(
        verbose_name='Название категории',
        max_length=50,
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Жанр произведения.
    Например: фантастика, сай-фай, рок и т.д.
    """
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=50,
    )
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name


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


class Genre_Title(models.Model):
    """
    Связка произведение-жанр.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre'
    )

    class Meta:
        verbose_name = 'Genre-Title'
        verbose_name_plural = 'Genre-Titles'

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    """
    Отзывы на произведения
    """
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review_author'
    )
    score = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
