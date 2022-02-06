import datetime as dt

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
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
        max_length=50,
        validators=[UniqueValidator(
            queryset=Category.objects.all(),
            message='Такая категория уже существует.'
        )]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Genre'.
    """
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(
            queryset=Genre.objects.all(),
            message='Такой жанр уже существует.'
        )]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoryDisplaySerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Category'.
    Используется на чтение внутри 'TitleDisplaySerializer'.
    """
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreDisplaySerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Genre'.
    Используется на чтение внутри 'TitleDisplaySerializer'.
    """
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Title'.
    Используется на запись.
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


class TitleDisplaySerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Title'.
    Используется на чтение.
    """
    category = CategoryDisplaySerializer(read_only=True)
    genre = GenreDisplaySerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField(read_only=True)

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        rating = reviews.aggregate(Avg('score'))
        if rating.get('score__avg') is None:
            return f'У {obj.name} пока нет оценок.'
        return rating.get('score__avg')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class SignUpSerializer(serializers.ModelSerializer):
    """
    Создает пользователей через API.
    """
    username = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

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
    username = serializers.CharField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

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
        self.fields['confirmation_code'] = serializers.CharField()
        del self.fields['password']  # Вместо пароля confirmation_code

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        if not default_token_generator.check_token(user,
                                                   attrs['confirmation_code']):
            raise serializers.ValidationError(
                'Неверный код подтверждения!')

        refresh = self.get_token(user)
        data = {'token': str(refresh.access_token), }

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
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        author = self.context.get('request').user
        title_id = get_object_or_404(
            Title,
            id=self.context.get('view').kwargs.get('title_id')
        )
        if (self.context.get('request').method == 'POST'
            and Review.objects.filter(title_id=title_id,
                                      author_id=author.id).exists()):
            raise serializers.ValidationError('fdfasfsaf')
        return data


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
        fields = ('id', 'text', 'author', 'pub_date',)

    def validate(self, data):
        get_object_or_404(
            Review,
            id=self.context.get('view').kwargs.get('review_id'),
            title_id=self.context.get('view').kwargs.get('title_id')
        )
        return data
