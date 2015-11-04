"""
    blog.permissions
    ================

    Custom Permissions for Blog App
"""
import logging

from rest_framework.permissions import BasePermission

logger = logging.getLogger('test_logger')


class ListRouteIsAdmin(BasePermission):
    """
    Custom Permission Class which authenticates a request for `list` route which we want only admins to see

    """

    def has_permission(self, request, view):
        if view.action == 'all_posts':
            #  check user is authenticated for 'list' route requests
            return request.user and (request.user.is_staff or request.user.is_superuser)
        return True
