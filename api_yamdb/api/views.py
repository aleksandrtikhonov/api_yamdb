from django.contrib.auth import get_user_model
from rest_framework import filters, generics, pagination, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Genre, Title

from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          MyTokenObtainPairSerializer, TitleSerializer,
                          UserSerializer)
from .viewsets import (CreateListRetrieveDeleteViewSet,
                       CreateUpdateListRetrieveDeleteViewSet)
from .permissions import IsAdminOrReadOnly

User = get_user_model()

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


class UserList(generics.ListCreateAPIView):
    """Обработка запросов к пользователям."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = pagination.PageNumberPagination


class MyTokenObtainPairView(TokenObtainPairView):
    """Обработка запросов токенов."""
    serializer_class = MyTokenObtainPairSerializer

class ReviewViewSet(CreateUpdateListRetrieveDeleteViewSet):
    """Обработка запросов к отзывам"""
    pass


class CommentViewSet(CreateUpdateListRetrieveDeleteViewSet):
    """Обработка запросов к комментариям на произведения"""
    pass

