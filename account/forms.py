from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['theme_preference']
        labels = {
            'theme_preference': 'Тема сайта'
        }

class SelfUserChangeForm(UserChangeForm):
    """
    Используется самим пользователем, не содержит поля role.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'photo', 'first_name', 'last_name',
                  'theme_preference')  # без 'role'
        labels = {
            'username': 'Имя пользователя (ник)',
            'email': 'Email',
            'photo': 'Фотография',
            'theme_preference': 'Тема',
        }