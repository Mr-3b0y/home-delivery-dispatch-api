from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from common.db import BaseModel
from math import radians, sin, cos, sqrt, atan2


class Driver(User, BaseModel):
    """
    Model representing a driver.
    """
    vehicle_plate = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=100)
    vehicle_year = models.PositiveIntegerField()
    vehicle_color = models.CharField(max_length=30)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    
    
    def __str__(self):
        return f"{self.user.username} - {self.vehicle_plate}"
    
    class Meta:
        app_label = 'drivers'
        verbose_name = _('Driver')
        verbose_name_plural = _('Drivers')
        
        
    def calculate_distance(self, latitude, longitude):
        """
        Calculate the distance from the driver's current location to the pickup address
        using the Haversine formula.
        Returns distance in kilometers.
        """
        
        # Earth radius in kilometers
        R = 6371.0
        
        # Convert latitude and longitude from decimal degrees to radians
        lat1 = radians(float(self.current_latitude))
        lon1 = radians(float(self.current_longitude))
        lat2 = radians(float(latitude))
        lon2 = radians(float(longitude))
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance