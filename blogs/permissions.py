from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Танҳо admin/superadmin метавонад POST, PUT, PATCH, DELETE кунад.
    Дигарон фақат GET доранд.
    """

    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS → барои ҳама
        if request.method in SAFE_METHODS:
            return True

        # POST, PUT, DELETE → фақат admin/superuser
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )
