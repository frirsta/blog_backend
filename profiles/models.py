from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/default.png')
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username
