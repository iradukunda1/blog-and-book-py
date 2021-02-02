from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.

class UserProfileManager(BaseUserManager):
    """hElP OUR DJANGO WORK WITH MY COSTUMER USER"""
    model = models

    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("User must have email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ User profile class inside our model """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    create_on = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # def __init__(self, email, name, is_active, create_on, is_staff):
    #     self.email = email
    #     self.name = name
    #     self.is_active = is_active
    #     self.create_on = create_on
    #     self.is_staff = is_staff

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class ProfileFeedItem(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    # def __init__(self, status_text, created_time):
    #     self.status_text = status_text
    #     self.created_time = created_time

    def __str__(self):
        return self.status_text
