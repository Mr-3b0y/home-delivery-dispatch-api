# from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from decimal import Decimal
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager


from common.db import BaseModel
from apps.users.models import User


class Address(models.Model):
    """
    Model representing an address.
    """
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses_created',
        null=True,
        blank=True
    )
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[0-9a-zA-Z\s-]+$',
                message=_('Enter a valid postal code. This value may contain only letters, numbers, spaces and hyphens.')
            )
        ]
    )
    coordinates = models.PointField(geography=True,
                                    srid=4326, db_index=True)
    reference = models.TextField(null=True, blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = GeoManager()
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}, {self.postal_code}"
    
    
    class Meta:
        app_label = 'addresses'
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        indexes = [
            models.Index(fields=['city', 'state', 'country']),
        ]

