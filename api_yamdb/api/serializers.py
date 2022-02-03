from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Category'.
    """
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Genre'.
    """
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Title'.
    """
    category = serializers.StringRelatedField(
        source='category_id',
        required=False,
        read_only=True,
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name',
            'year', 'category',
            'category_id'
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

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
    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if default_token_generator.check_token(user,
                                               data['confirmation_code']):
            raise serializers.ValidationError(
                'Неверный код подтверждения!')
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
