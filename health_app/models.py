from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RealEstate(models.Model):
    FURNISHING_CHOICES = [
        ('unfurnished', 'Unfurnished'),
        ('semi-furnished', 'Semi-Furnished'),
        ('furnished', 'Furnished'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField()
    area = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    stories = models.IntegerField()
    mainroad = models.BooleanField()
    guestroom = models.BooleanField()
    basement = models.BooleanField()
    hotwaterheating = models.BooleanField()
    airconditioning = models.BooleanField()
    parking = models.IntegerField()
    prefarea = models.BooleanField()
    furnishingstatus = models.CharField(max_length=15, choices=FURNISHING_CHOICES)

    def __str__(self):
        return f"RealEstate(id={self.id}, price={self.price}, area={self.area}), user={self.user.username}"