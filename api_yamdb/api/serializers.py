from reviews.models import Category
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class CategorySerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Category'.
    """

    class Meta:
        model = Category
        fields = '__all__'
