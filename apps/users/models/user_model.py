from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)



class User(AbstractUser, PermissionsMixin):
    """
    Custom user model that extends the default Django user model.
    """
    phone_number = models.CharField(max_length=15,
                                    unique=True,
                                    validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
                                    error_messages={
                                        'unique': "A user with that phone number already exists.",  
                                    })
    # is_driver = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()
    
    class Meta:
        app_label = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.username