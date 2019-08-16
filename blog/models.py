import os
from datetime import datetime as dt
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def path_and_rename(instance, filename):
    upload_to = 'avatar'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.user.username, ext)
    return os.path.join(upload_to, filename)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='comments')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    reply_to = models.ForeignKey('blog.Comment', on_delete=models.SET_NULL, null=True, default=None)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email =  models.EmailField(unique=True, null=True)
    avatar = models.ImageField(default='avatars/default.png', upload_to='avatars/users_avatars/', blank=True)

    def __str__(self):
        return self.user.username