from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

from common.db import BaseModel
from apps.users.models import User
from apps.drivers.models import Driver
from apps.addresses.models import Address


class Service(BaseModel):
    STATUS_CHOICES = (
        ('IN_PROGRESS', 'In progress'),
        ('COMPLETED', 'Completed'),
    )
    
    client = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='services')
    driver = models.ForeignKey(Driver,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='driver_services')
    pickup_address = models.ForeignKey(Address,
                                       on_delete=models.PROTECT,
                                       related_name='pickup_services')
    status = models.CharField(max_length=15,
                              choices=STATUS_CHOICES,
                              default='IN_PROGRESS')
    distance_km = models.DecimalField(max_digits=10,
                                      decimal_places=2,
                                      null=True,
                                      blank=True,
                                      validators=[MinValueValidator(Decimal('0'))])
    estimated_arrival_minutes = models.PositiveIntegerField(null=True,
                                                            blank=True)
    
    
    class Meta:
        app_label = 'services'
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        indexes = [
            models.Index(fields=['status']),
        ]
