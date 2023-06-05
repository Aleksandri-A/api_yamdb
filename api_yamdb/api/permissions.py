from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorAdminModeratorOrReadOnlyPermission(BasePermission):
    message = (
        'Проверка пользователя является ли он админом, автором или модератором'
        'или автором объекта, иначе только режим чтения'
    )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.role == 'admin'
                    or request.user.role == 'moderator'
                    or obj.author == request.user))


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.role == 'admin'
            or request.user.is_superuser
        )
