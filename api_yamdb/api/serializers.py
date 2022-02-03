import datetime as dt

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
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


class SignUpSerializer(serializers.ModelSerializer):
    """
    Создает пользователей через API.
    """
    username = serializers.CharField(max_length=150, allow_blank=False)
    email = serializers.EmailField(max_length=254, allow_blank=False)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Измените username!')
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'User'.
    """
    username = serializers.CharField(max_length=150, allow_blank=False)
    email = serializers.EmailField(max_length=254, allow_blank=False)

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        model = User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Новый сериалайзер для получения токена.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        del self.fields['password']
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if default_token_generator.check_token(user,
                                               data['confirmation_code']):
            raise serializers.ValidationError(
                'Неверный код подтверждения!')

        refresh = self.get_token(user)
        data['token'] = str(refresh.access_token)

        return data


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
