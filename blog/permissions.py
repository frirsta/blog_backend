from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsActiveUser(BasePermission):
    """
    Allows access only to active users.
    """

    def has_permission(self, request, view):
        if not request.user.is_active:
            raise PermissionDenied("User account is disabled.")
        return True
