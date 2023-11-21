from django.urls import path
from django.contrib.auth import views as auth_views
# from .forms import CustomAuthenticationForm
from . import views

app_name='setting'

urlpatterns = [
    path('main/', views.main, name='main'),
]