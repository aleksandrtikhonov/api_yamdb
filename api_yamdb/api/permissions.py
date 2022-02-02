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
