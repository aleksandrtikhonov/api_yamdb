from rest_framework import permissions


class TitlePermission(permissions.BasePermission):
    """
    Кастмоный пермишен для Title.
    """
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        if request.method == 'PUT':
            return False
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    POST/DELETE запросы доступны только администратору либо суперюзеру.
    """
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
        )


class IsAdmin(permissions.BasePermission):
    """
    Доступ только администратору.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.is_superuser
                or request.user.role == 'admin')


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Доступ на изменение только автору.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.role == 'moderator'
