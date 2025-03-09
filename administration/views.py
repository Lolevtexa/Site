from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden
from .forms import CreateUserByEmailForm, CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .utils import generate_temp_username, generate_temp_password

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

    return render(request, 'administration/create_account_minimal.html', {'form': form})

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
    return render(request, 'administration/create_account.html', {'form': form})

@login_required
@user_passes_test(admin_check)
def manage_accounts(request):
    # Получаем список всех пользователей
    users = CustomUser.objects.all()
    return render(request, 'administration/manage_accounts.html', {'users': users})

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
    return render(request, 'administration/edit_account.html', {'form': form, 'user_to_edit': user_to_edit})

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