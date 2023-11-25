from django.urls import path
from django.contrib.auth import views as auth_views
# from .forms import CustomAuthenticationForm
from . import views

app_name='setting'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('body/', views.body, name='body'),
    path('goal/', views.goal, name='goal'),
    path('myinfo/', views.myinfo, name='myinfo'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
]