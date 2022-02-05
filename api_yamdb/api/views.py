from asyncio.windows_events import NULL
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, pagination, permissions, viewsets
from django.contrib.auth.tokens import default_token_generator
from rest_framework import (filters, generics, pagination,
                            permissions, status, viewsets)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from reviews.models import Category, Genre, Review, Title
from django.shortcuts import get_object_or_404
from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          MyTokenObtainPairSerializer, TitleSerializer,
                          UserSerializer, ReviewSerializer, CommentSerializer,
                          SignUpSerializer)
from .viewsets import (CreateUpdateListRetrieveDeleteViewSet,
                       CreateListDeleteViewSet)

User = get_user_model()


class CategoryViewSet(CreateListDeleteViewSet):
    """Обработка запросов к категориям."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDeleteViewSet):
    """Обработка запросов к жанрам."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Обработка запросов к произведениям."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class UserList(generics.ListCreateAPIView):
    """Обработка запросов к пользователям."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = pagination.PageNumberPagination


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """Обработка запросов к пользователям."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,
                                username=self.kwargs['username'])
        return obj


class UserSelfDetail(generics.RetrieveUpdateAPIView):
    """Обработка запросов к своему пользователю."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,
                                username=self.request.user.username)
        return obj

    def perform_update(self, serializer):
        user_role = self.request.user.role
        request_role = serializer.validated_data.get('role')
        if (user_role == 'user'
                and request_role is not NULL
                and request_role != user_role):
            serializer.validated_data['role'] = 'user'
        serializer.save()


class MyTokenObtainPairView(TokenObtainPairView):
    """Обработка запросов токенов."""
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = (permissions.AllowAny,)


@api_view(['POST', ])
@permission_classes((permissions.AllowAny, ))
def send_token(request):
    """
    Отправка кода подтверждения по почте.
    """
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            # Создадим пользователя
            serializer.save()
            # Отправим письмо с кодом подтверждения
            user = get_object_or_404(User,
                                     username=serializer.data['username'])
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Подтверждение регистрации пользователя',
                f'Код подтверждения: {confirmation_code}',
                'from@example.com',  # "От кого"
                [serializer.data['email']],  # "Кому"
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(CreateUpdateListRetrieveDeleteViewSet):
    """Обработка запросов к отзывам"""
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # IsAdminOrReadOnly, IsAuthorOrReadOnly
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
