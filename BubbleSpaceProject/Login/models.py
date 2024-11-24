from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import os

class UsersAccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class Users_Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    birthDate = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsersAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fname', 'lname',"birthDate","gender"]

    def set_password(self, raw_password):
        super().set_password(raw_password)

    @property
    def age(self):
        today = date.today()
        return (today.year - self.birthDate.year) - ((today.month, today.day) < (self.birthDate.month, self.birthDate.day))

    def __str__(self):
        return self.username
    def delete(self, *args, **kwargs):
        # Delete the profile picture from storage when deleting the user
        if self.profile_picture and self.profile_picture.name != 'profile_pictures/default.svg':
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
        super().delete(*args, **kwargs)
