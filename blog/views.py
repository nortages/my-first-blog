from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.cache import never_cache
from django.utils import timezone
# from django.views.defaults import permission_denied

from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm, UserForm, ProfileForm, Login_form


def only_creator(view, pk, staff):
    def wrapper(request, *args, **kwargs):
        if request.user == staff.author:
            return HttpResponseRedirect(url)
        return view(request, *args, **kwargs)
    return wrapper


def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.order_by('-created_date')
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form, 'action': 'Create'})
    
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if (not request.user.is_superuser) and (request.user != post.author):
        raise PermissionDenied
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'action': 'Edit'})
    
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if (not request.user.is_superuser) and (request.user != post.author):
        raise PermissionDenied
    post.delete()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if (not request.user.is_superuser) and (request.user != comment.author):
        raise PermissionDenied
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def register(request):
    errors = {'user_form': '', 'profile_form': ''}
    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            # group = Group.objects.get(name='auth_users')
            # user.groups.add(group)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
                ext = profile.avatar.name.split('.')[1]
                profile.avatar.name = request.POST['username'] + '.' + ext
            profile.save()
            return redirect('login')
        else:
            print(user_form.errors, profile_form.errors)
            errors = {'user_form': user_form.errors, 'profile_form': profile_form.errors}
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request,'registration/registration.html',
                          {'user_form': user_form,
                           'profile_form': profile_form,
                           'errors': errors})

def profile(request, username=None):
    if username == None:
        username = request.user.username
    profile = get_object_or_404(User, username=username).profile
    posts = profile.user.posts.order_by('-created_date')
    return render(request, 'blog/profile.html', {'profile': profile, 'posts': posts})

@login_required
def profile_edit(request, username=None):
    if username == None:
        username = request.user.username
    user = get_object_or_404(User, username=username)
    profile = user.profile
    if request.user != user:
        raise PermissionDenied
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', username=request.POST['username'])
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'blog/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})