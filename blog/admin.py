from django.contrib import admin
from .models import Post, Comment, Profile, User

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)