from django.contrib import admin
from apps.addresses.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    Admin view for the Address model.
    """
    list_display = ('id', 'street', 'city', 'state', 'country', 'postal_code', 'created_by')
    list_filter = ('city', 'state', 'country')
    search_fields = ('street', 'city', 'state', 'country', 'postal_code', 'reference')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('created_by',)
