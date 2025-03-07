# website/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)      # renamed from "zip"
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)

    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)  # renamed from "password1"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
