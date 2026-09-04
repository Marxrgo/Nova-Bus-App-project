from django.db import models

# Create your models here.

# accounts/models.py
from django.contrib.auth.models import AbstractUser ##TODO review this
from loops.models import Looptype

class User(AbstractUser):
    managed_loop = models.CharField(
        max_length=10, choices=Looptype.choices, null=True, blank=True
    )