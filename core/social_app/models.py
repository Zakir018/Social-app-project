from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser





# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length= 50)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=15)
    country = models.CharField(max_length=25)
    profile_picture = models.ImageField(upload_to='profile-images/',)

    def __str__(self):
        return self.first_name



