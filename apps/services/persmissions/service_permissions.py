from rest_framework import permissions


class ServicePermission(permissions.BasePermission):
    """
    Custom permission for Service model:
    1. Only admins, the client who created the service, or the assigned driver can view the service
    2. Only admins or the client who created the service can edit the service
    3. Only the assigned driver can update the service status (complete action)
    """
    
    def has_permission(self, request, view):
        # Allow authenticated users to list and create services
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin permissions - can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Client permissions - can view and edit their own services
        if obj.client == request.user:
            if view.action == 'complete':
                # Clients cannot use the complete action
                return False
            return True
        
        # Driver permissions - can view and use the complete action
        if hasattr(obj, 'driver') and obj.driver and obj.driver.user_ptr_id == request.user.id:
            if request.method in permissions.SAFE_METHODS or view.action == 'complete':
                return True
            return False
        
        # For all other users
        return False