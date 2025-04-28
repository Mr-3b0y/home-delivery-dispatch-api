from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    Permission class that allows:
    - Admin users to perform any action
    - Regular users to only retrieve and update their own driver information
    - Only admins can see the full list of drivers
    """
    
    def has_permission(self, request, view):
        """
        Define permission for listing drivers:
        - Only admins can list all drivers
        - Everyone can access retrieve, update, and partial_update (will be filtered in has_object_permission)
        - Only admins can create and delete drivers
        """
        # If user is admin, allow any action
        if request.user.is_staff or request.user.is_superuser:
            return True
            
        # For list action, only allow admins
        if view.action == 'list':
            return False
            
        # For retrieve, update, partial_update allow any authenticated user (will check object permissions next)
        if view.action in ['retrieve', 'update', 'partial_update']:
            return True
            
        # For other actions (create, destroy), only allow admins
        return False
        
    def has_object_permission(self, request, view, obj):
        """
        Define permissions for specific driver objects:
        - Admin can perform any action on any driver
        - Regular users can only retrieve and update their own driver information
        """
        # Admin can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True
            
        # Non-admin users can only access their own driver information
        return obj.id == request.user.id