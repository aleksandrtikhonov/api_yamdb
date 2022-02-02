from reviews.models import Category, Genre, Title
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
