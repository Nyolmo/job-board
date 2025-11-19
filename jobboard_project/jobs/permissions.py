from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCompanyAdminOrReadOnly(BasePermission):
    """
    Only job owners (users who posted) can update/delete.
    Everyone can read.

    """

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True


        return obj.posted_by == request.user