from reviews.models import Category, Genre
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


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
