from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager
from apps.users.models import User
from common.db import BaseModel


class Driver(User):
    """
    Model representing a driver.
    """
    vehicle_plate = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=100)
    vehicle_year = models.PositiveIntegerField()
    vehicle_color = models.CharField(max_length=30)
    location_coordinates = models.PointField(geography=True,
                                            srid=4326, db_index=True)
    is_available = models.BooleanField(default=True)
    
    # objects = GeoManager()
    
    def __str__(self):
        return f"{self.username} - {self.vehicle_plate}"
    
    class Meta:
        app_label = 'drivers'
        verbose_name = _('Driver')
        verbose_name_plural = _('Drivers')
        