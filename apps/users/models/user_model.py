from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin



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
    is_driver = models.BooleanField(default=False)
    is_client = models.BooleanField(default=True)
    
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()

    def __str__(self):
        return self.username