from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=30)
    timestamp = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.content