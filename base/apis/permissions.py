from rest_framework.permissions import BasePermission


class AppOwnPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Checks if App-Own key is in request, App-Own key will be passed from App requests.
        """
        if "App-Own" in request.headers:
            return True
        return False
