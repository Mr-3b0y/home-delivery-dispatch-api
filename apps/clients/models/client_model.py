from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Client(User):
    default_address = models.ForeignKey('Address',
                                        on_delete=models.SET_NULL,
                                        null=True, blank=True)
    
    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')