from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=15)
    country = models.CharField(max_length=25)
    cover_picture = models.ImageField(null=True, blank=True, upload_to='cover-images/')
    profile_picture = models.ImageField(  null=True, blank=True, upload_to='profile-images/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length= 150)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    image = models.ImageField(  null=True, blank=True, upload_to='posts-img/')

    def is_liked_by_user(self, user):
        return self.likes.filter(user = user).exists()

    def total_likes(self):
        return self.likes.count()
    
    def total_comments(self):
        return self.comments.count()

    def __str__(self):
        return self.user.username + ' - ' + self.body
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length= 150)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.user} comment {self.post}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} like {self.post}"
    
class Social_group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    name = models.CharField(max_length= 100)
    description = models.CharField(max_length= 200)
    profile_img = models.ImageField(null= True, blank= True, upload_to="group_profile")
    cover_img = models.ImageField(null= True, blank= True, upload_to= "group_coverpic")

    def __str__(self) :
        return  self.name

