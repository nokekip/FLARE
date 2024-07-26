import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# custom user model
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
