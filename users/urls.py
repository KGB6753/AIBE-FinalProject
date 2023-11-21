from django.urls import path
from django.contrib.auth import views as auth_views
# from .forms import CustomAuthenticationForm
from . import views

app_name='users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signupOK/', views.signupOK, name='signupOK'),
    path('login/', views.login_user, name='login'),
    path('loginOK/', views.loginOK, name='loginOK'),
    path('logout/',views.logout_user,name='logout'),
]