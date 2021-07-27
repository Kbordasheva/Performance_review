from rest_framework import permissions


class IsManagerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return self._has_permission(request)

    def has_object_permission(self, request, view, obj):
        return self._has_permission(request)

    @staticmethod
    def _has_permission(request):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_manager or request.user.is_superuser
