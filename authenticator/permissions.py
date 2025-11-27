from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Permission check for super admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   (request.user.role == 'superadmin' or request.user.is_superuser))


class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Permission check for admin and super admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                   (request.user.role in ['admin', 'superadmin'] or request.user.is_superuser))