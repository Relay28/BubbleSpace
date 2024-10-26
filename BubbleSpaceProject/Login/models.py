from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UsersAccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Users_Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    gender = models.CharField(max_length=20)
    birthDate = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsersAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [ 'fname', 'lname',]

    def set_password(self, raw_password):
        super().set_password(raw_password)

    @property
    def age(self):
        today = date.today()
        return (today.year - self.birthDate.year) - ((today.month, today.day) < (self.birthDate.month, self.birthDate.day))

    def __str__(self):
        return self.username
