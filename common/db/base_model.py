from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields and methods for all models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']