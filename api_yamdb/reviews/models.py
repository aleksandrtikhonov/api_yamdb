import datetime as dt

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Новая модель пользователя.
    Добавлены роли и графа О себе.
    """
    USER_ROLES = [
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(
        max_length=9,
        choices=USER_ROLES,
        default='user',
    )
    bio = models.TextField('О себе', blank=True)


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
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Жанр произведения.
    Например: фантастика, сай-фай, рок и т.д.
    """
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведение.
    Например: название фильма, книги, песни и т.д.
    """
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выхода',
        validators=[
            max_value_current_year
        ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title'
    )
    genre = models.ManyToManyField(
        Genre,
        through='Genre_Title'
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-id']

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
        ordering = ['-id']

    def __str__(self):
        title = self.title.name
        genre = self.genre.name
        return f'{title} - {genre}'


class Review(models.Model):
    """
    Отзыв на произведения
    """
    title = models.ForeignKey(
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
    # Поле для хранения оценки пользователя произведения
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


class Comment(models.Model):
    """
    Комментарий к отзыву на произведение
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_author'
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
