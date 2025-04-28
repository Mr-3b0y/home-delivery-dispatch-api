from django.contrib import admin
from apps.services.models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Service model.
    """
    list_display = ('id', 'client', 'driver', 'pickup_address', 'status', 
                    'distance_km', 'estimated_arrival_minutes', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__username', 'driver__user__username', 'pickup_address__street')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('client', 'driver', 'pickup_address', 'status')
        }),
        ('Service Details', {
            'fields': ('distance_km', 'estimated_arrival_minutes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
