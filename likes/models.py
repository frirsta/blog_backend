from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
        unique_together = ['user', 'post']

    def __str__(self):
        return f"{self.user} by {self.post}"
