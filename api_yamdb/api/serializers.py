import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Category'.
    """
    slug = serializers.SlugField(
        max_length=100,
        validators=[UniqueValidator(
            queryset=Category.objects.all(),
            message='Такая категория уже существует.'
        )]
    )

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Genre'.
    """
    slug = serializers.SlugField(
        max_length=100,
        validators=[UniqueValidator(
            queryset=Genre.objects.all(),
            message='Такой жанр уже существует.'
        )]
    )

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Title'.
    """
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    def validate_year(self, value):
        current_year = dt.date.today().year
        if 0 < value < current_year:
            return value
        raise serializers.ValidationError(
            'Проверьте год выхода'
        )

    class Meta:
        model = Title
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category')
            )
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        model = User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # token['name'] = user.name
        # ...

        return token


class ReviewSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Review'.
    """
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Comment'.
    """
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
