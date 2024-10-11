from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = CloudinaryField(
        'image', blank=True, null=True, default='blog_media/profile_pictures/default.png')
    cover_picture = CloudinaryField(
        'image', blank=True, null=True, default='blog_media/cover_pictures/default.png')
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username
