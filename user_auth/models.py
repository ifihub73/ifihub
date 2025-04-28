from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUser(AbstractUser):
    phone = PhoneNumberField(region='NG',blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)

