from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden
from .forms import (CreateUserByEmailForm, SelfUserChangeForm, 
                    CustomUserCreationForm, UserSettingsForm, 
                    CustomUserChangeForm)
from .models import CustomUser
from .utils import generate_temp_username, generate_temp_password

def index(request):
    return render(request, 'accounts/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'accounts/login.html', {'error': 'Неверное имя пользователя или пароль'})
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    # Если must_change_credentials = True, выводим предупреждение
    # (можно передать в шаблон флаг, можно просто в шаблоне проверить user.must_change_credentials)
    return render(request, 'accounts/profile.html', {'user': user})

@login_required
def settings_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=user)
    return render(request, 'accounts/settings.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = SelfUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Если пользователь меняет имя пользователя (не temp_username) 
            # или пароль (не temp_password), сбрасываем флаг:
            # Т.к. пароль мы не можем сравнить напрямую, 
            # проще считать, что если пользователь хотя бы раз изменил логин,
            # можно снять флаг (или использовать другую логику).
            user.must_change_credentials = False
            user.save()
            return redirect('profile')
    else:
        form = SelfUserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def admin_check(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(admin_check)
def create_account_minimal(request):
    if request.method == 'POST':
        form = CreateUserByEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Генерируем временные логин/пароль
            temp_username = generate_temp_username()
            while CustomUser.objects.filter(username=temp_username).exists():
                temp_username = generate_temp_username()

            temp_password = generate_temp_password()


            # Создаём пользователя
            new_user = CustomUser.objects.create_user(
                username=temp_username,
                email=email,
                password=temp_password,
            )
            # Указываем, что нужно сменить имя/пароль
            new_user.must_change_credentials = True
            new_user.save()

            # Отправляем письмо
            subject = "Ваш новый аккаунт"
            message = (
                f"Здравствуйте!\n\n"
                f"Для вас был создан аккаунт на сайте lolevtexa.ru.\n"
                f"Временный логин: {temp_username}\n"
                f"Временный пароль: {temp_password}\n\n"
                f"Рекомендуем сменить имя пользователя и пароль при первом входе.\n"
                f"С уважением,\nАдминистрация сайта"
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('manage_accounts')  # или на любую нужную страницу
    else:
        form = CreateUserByEmailForm()

    return render(request, 'accounts/create_account_minimal.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def create_account(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            # Дополнительно, если роль 'admin' → is_staff = True
            if new_user.role == 'admin':
                new_user.is_staff = True
            new_user.save()
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/create_account.html', {'form': form})

def admin_check(user):
    # Проверяем, что пользователь - администратор (is_staff или is_superuser)
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(admin_check)
def manage_accounts(request):
    # Получаем список всех пользователей
    users = CustomUser.objects.all()
    return render(request, 'accounts/manage_accounts.html', {'users': users})

@login_required
@user_passes_test(admin_check)
def edit_account(request, user_id):
    # Редактируем другого пользователя
    user_to_edit = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            # Если роль 'admin', делаем is_staff=True, иначе is_staff=False (по желанию)
            updated_user = form.save(commit=False)
            if updated_user.role == 'admin':
                updated_user.is_staff = True
            else:
                # Если хотите, чтобы только admin-роль имела is_staff
                updated_user.is_staff = False
            updated_user.save()
            return redirect('manage_accounts')
    else:
        form = CustomUserChangeForm(instance=user_to_edit)
    return render(request, 'accounts/edit_account.html', {'form': form, 'user_to_edit': user_to_edit})

@login_required
@user_passes_test(admin_check)
def delete_account(request, user_id):
    # Удаляем другого пользователя
    user_to_delete = get_object_or_404(CustomUser, pk=user_id)
    # Чтобы случайно не удалить самого себя, можно добавить проверку:
    if user_to_delete == request.user:
        return HttpResponseForbidden("Нельзя удалить самого себя.")
    user_to_delete.delete()
    return redirect('manage_accounts')