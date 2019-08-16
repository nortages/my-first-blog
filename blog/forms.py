from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from .models import Post, Comment, Profile


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title', 'id':'inputTitle'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'autofocus':True, 'class':'form-control', 'placeholder':'Text', 'id':'inputText'}))
    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'autofocus':True, 'class':'form-control', 'placeholder':'Comment text', 'id':'inputComment'}))
    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['username'].widget.attrs.update({'maxlength':"25", 'autofocus': True, 'class': 'form-control', 'placeholder':'Username', 'id':'inputUsername'})
        self.fields['password1'].widget.attrs.update({'class':'form-control', 'placeholder':'Password', 'id':'inputPassword1'})
        self.fields['password2'].widget.attrs.update({'class':'form-control', 'placeholder':'Password confirmation', 'id':'inputPassword2'})


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'id':'inputEmail'}))
    class Meta:
        model = Profile
        fields = ('email', 'avatar',)


class Login_form(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['username'].widget.attrs.update({'maxlength':"25", 'autofocus': True, 'class': 'form-control', 'placeholder':'Username', 'id':'inputUsername'})
        self.fields['password'].widget.attrs.update({'class':'form-control', 'placeholder':'Password', 'id':'inputPassword'})

