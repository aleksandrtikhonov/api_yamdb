from rest_framework import filters, pagination, permissions, viewsets
from reviews.models import Category, Genre, Title
from .viewsets import (CreateListRetrieveDeleteViewSet,
                       CreateUpdateListRetrieveDeleteViewSet)
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(CreateListRetrieveDeleteViewSet):
    """Обработка запросов к категориям."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListRetrieveDeleteViewSet):
    """Обработка запросов к жанрам."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Обработка запросов к произведениям."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny,)


class ReviewViewSet(CreateUpdateListRetrieveDeleteViewSet):
    """Обработка запросов к отзывам"""
    pass


class CommentViewSet(CreateUpdateListRetrieveDeleteViewSet):
    """Обработка запросов к комментариям на произведения"""
    pass
