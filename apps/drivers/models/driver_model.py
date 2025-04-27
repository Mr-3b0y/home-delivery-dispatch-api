from django.db import models

from apps.users.models import User
from common.db import BaseModel


class Driver(User, BaseModel):
    
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
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'