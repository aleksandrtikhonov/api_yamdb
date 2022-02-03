from django.contrib.auth import get_user_model
from rest_framework import filters, generics, pagination, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Genre, Review, Title
from django.shortcuts import get_object_or_404
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          MyTokenObtainPairSerializer, TitleSerializer,
                          UserSerializer, ReviewSerializer, CommentSerializer)
from .viewsets import (CreateListRetrieveDeleteViewSet,
                       CreateUpdateListRetrieveDeleteViewSet,
                       CreateListDeleteViewSet)

User = get_user_model()


class CategoryViewSet(CreateListDeleteViewSet):
    """Обработка запросов к категориям."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDeleteViewSet):
    """Обработка запросов к жанрам."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (permissions.AllowAny)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Обработка запросов к произведениям."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #permission_classes = (IsAdminOrReadOnly,)
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
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly, IsAuthorOrReadOnly
    )

    def get_queryset(self, **kwargs):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id',)
        )
        return title.reviews.all()

    def perform_create(self, serializer, **kwargs):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id',)
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(CreateUpdateListRetrieveDeleteViewSet):
    """Обработка запросов к комментариям на произведения"""
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly, IsAuthorOrReadOnly
    )

    def get_queryset(self, **kwargs):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id',)
        )
        return review.comment.all()

    def perform_create(self, serializer, **kwargs):
        serializer.save(
            author=self.request.user,
            review_id=self.kwargs.get('review_id',)
        )
