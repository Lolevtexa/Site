from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CreateUserByEmailForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.USER  # Назначаем обычного пользователя
        if commit:
            user.save()
        return user

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