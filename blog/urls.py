from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.staticfiles.urls import static

from . import views
from .forms import Login_form


class CustomLoginView(LoginView):
    authentication_form = Login_form
    

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/add_comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('accounts/register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/<str:username>', views.profile_edit, name='profile_edit'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]


