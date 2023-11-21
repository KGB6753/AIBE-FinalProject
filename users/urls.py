from django.urls import path
from django.contrib.auth import views as auth_views
# from .forms import CustomAuthenticationForm
from . import views

app_name='users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signupOK/', views.signupOK, name='signupOK'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html',authentication_form=CustomAuthenticationForm), name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', views.login_user, name='login'),
    path('loginOK/', views.loginOK, name='loginOK'),
    path('logout/',views.logout_user,name='logout'),
    # path('logoutOK/', views.logout_OK, name='loginOK'),
]