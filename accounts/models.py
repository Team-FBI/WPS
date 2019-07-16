from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="user_image/profile/%Y/%m/%d/", blank=True)
    def __str__(self):
        return self.username
