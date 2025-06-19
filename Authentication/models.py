from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)


    def __str__(self):
        return f"{self.username}- {self.full_name}"
