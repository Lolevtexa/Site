from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'photo', 'role', 'theme_preference')
        labels = {
            'username': 'Имя пользователя (ник)',
            'email': 'Email',
            'photo': 'Фотография',
            'role': 'Роль',
            'theme_preference': 'Тема',
        }

class CustomUserChangeForm(UserChangeForm):
    """
    Используется администратором для редактирования
    любого пользователя, включая роль.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'photo', 'first_name', 'last_name',
                  'role', 'theme_preference')
        labels = {
            'username': 'Имя пользователя (ник)',
            'email': 'Email',
            'photo': 'Фотография',
            'role': 'Роль',
            'theme_preference': 'Тема',
        }


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