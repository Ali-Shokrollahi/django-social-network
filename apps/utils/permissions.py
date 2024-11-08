from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAuthenticatedReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Other authenticated users are only able to get.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return obj.owner == request.user.profile


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
