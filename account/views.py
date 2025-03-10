from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SelfUserChangeForm, UserSettingsForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('account:profile')
        else:
            return render(request, 'account/login.html', {'error': 'Неверное имя пользователя или пароль'})
    return render(request, 'account/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('account:login')

@login_required
def profile(request):
    user = request.user
    # Если must_change_credentials = True, выводим предупреждение
    # (можно передать в шаблон флаг, можно просто в шаблоне проверить user.must_change_credentials)
    return render(request, 'account/profile.html', {'user': user})

@login_required
def settings_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account:settings')
    else:
        form = UserSettingsForm(instance=user)
    return render(request, 'account/settings.html', {'form': form})

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
            return redirect('account:profile')
    else:
        form = SelfUserChangeForm(instance=request.user)
    return render(request, 'account/edit_profile.html', {'form': form})
