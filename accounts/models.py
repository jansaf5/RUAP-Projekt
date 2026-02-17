from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[
        ('M', 'Male'), 
        ('F', 'Female')
        ], blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.user.first_name} {self.user.last_name}"