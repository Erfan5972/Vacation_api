from rest_framework.permissions import BasePermission, IsAdminUser, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only administrators to perform write operations,
    while allowing all users to perform read-only operations.
    """

    def has_permission(self, request, view):
        # Allow all users to perform safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Allow only admin users to perform write operations (POST, PUT, PATCH, DELETE)
        return request.user and request.user.is_superuser
