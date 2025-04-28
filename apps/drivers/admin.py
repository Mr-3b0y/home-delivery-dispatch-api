from django.contrib import admin

# Register your models here.
from apps.drivers.models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """Admin view for Driver model."""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'vehicle_model', 'vehicle_year', 'vehicle_color', 'is_available')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_available',)
    ordering = ('username',)
    readonly_fields = ('date_joined',)
    
    def get_queryset(self, request):
        """Override to include related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('user')