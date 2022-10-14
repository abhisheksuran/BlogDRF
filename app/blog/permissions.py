from rest_framework import permissions

class EditOwnPost(permissions.BasePermission):
    """User can edit its own post only"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author.id == request.user.id

class EditOwnComment(permissions.BasePermission):
    """User can edit its own comment only"""


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id


class EditOwnReply(permissions.BasePermission):
    """User can edit its own reply only"""


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id


class UpdateOwnTag(permissions.BasePermission):
    """User can edit its own tags"""
    def has_object_permission(self, request, view, obj):
 
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id