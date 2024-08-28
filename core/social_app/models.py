from django.db import models
from django.contrib.auth.models import User






# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length= 50)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=15)
    country = models.CharField(max_length=25)
    profile_picture = models.ImageField(  null=True, blank=True, upload_to='profile-images/')

    def __str__(self):
        return self.first_name
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
class Post(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    body = models.CharField(max_length= 150)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    image = models.ImageField(  null=True, blank=True, upload_to='posts-img/')

    def __str__(self):
        return self.user.username



