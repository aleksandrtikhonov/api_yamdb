from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    POST/DELETE запросы доступны только администратору.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
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
    Доступ на изменение только автору
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
