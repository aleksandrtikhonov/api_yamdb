from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, UserList

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path('v1/users/', UserList.as_view()),
]
