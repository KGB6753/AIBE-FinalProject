from django import forms
from .models import Menu


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['menu_weight', 'menu_date', 'menu_category', 'menu_food', 'menu_photo', 'menu_user']
        widgets = {
            'menu_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'menu_photo': forms.Select(attrs={'required': False}),
        }
