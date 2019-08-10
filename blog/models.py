import os
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def path_and_rename(instance, filename):
    upload_to = 'profile_pics'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.user.username, ext)
    return os.path.join(upload_to, filename)

# @receiver(post_delete, sender=Post)
# def photo_post_delete_handler(sender, **kwargs):
#     listingImage = kwargs['instance']
#     storage, path = listingImage.image.storage, listingImage.image.path
#     storage.delete(path)


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
    reply_to = models.ForeignKey('blog.Comment', on_delete=models.SET_NULL, default=None, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Profile(models.Model):
    email =  models.EmailField(unique=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(default='profile_pics/default.png', upload_to=path_and_rename, blank=True)

    def __str__(self):
        return self.user.username