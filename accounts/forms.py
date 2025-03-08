from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'photo')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'photo', 'first_name', 'last_name')

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['theme_preference']
        labels = {
            'theme_preference': 'Тема сайта'
        }