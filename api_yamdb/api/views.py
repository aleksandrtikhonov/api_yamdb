from django.shortcuts import get_object_or_404
from rest_framework import filters, pagination, permissions, viewsets

from reviews.models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Обработка запросов к категориям."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
