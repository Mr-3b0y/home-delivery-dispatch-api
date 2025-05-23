from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AddressesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.addresses'
    verbose_name = _('Addresses')
    # Using a unique label to avoid conflicts
    label = 'addresses'