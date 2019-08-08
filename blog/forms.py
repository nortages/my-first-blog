from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Post, Comment, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('username', 'password1', 'password2',)


class ProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('email', 'profile_pic',)


class Login_form(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username', 'password')
