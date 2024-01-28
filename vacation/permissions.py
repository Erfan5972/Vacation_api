from rest_framework.permissions import BasePermission


class CanCreateVacationResponse(BasePermission):
    def has_permission(self, request, view):
        role = request.user.role

        if role == 'manager' and view.kwargs.get('node_id') != 3:
            return False

        if role == 'technical_manager' and view.kwargs.get('node_id') != 2:
            return False

        return False