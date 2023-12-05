from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일ID")
    nickname = forms.CharField(label="닉네임")
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "nickname")

# class CustomAuthenticationForm(AuthenticationForm):
#
#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'password']

