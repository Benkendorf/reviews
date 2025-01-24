from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """Доступ только для администраторов."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin