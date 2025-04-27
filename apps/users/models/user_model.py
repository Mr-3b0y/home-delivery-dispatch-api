from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    is_driver = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)

    def __str__(self):
        return self.username