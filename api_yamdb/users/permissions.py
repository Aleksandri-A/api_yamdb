from rest_framework import permissions


class AuthorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or (
            request.user.is_authenticated
            and (request.method == "PATCH" or request.method == "GET")
        )

    def has_object_permission(self, request, view, obj):
        if (obj.author == request.user or request.user.is_staff):
            return True
