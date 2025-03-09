from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_account/', views.create_account, name='create_account'),

    # Страница управления аккаунтами
    path('manage_accounts/', views.manage_accounts, name='manage_accounts'),
    path('edit_account/<int:user_id>/', views.edit_account, name='edit_account'),
    path('delete_account/<int:user_id>/', views.delete_account, name='delete_account'),

    # Добавляем страницу смены пароля
    path('password/', auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html"
        ), name='password_change'),
    path('password/done/', auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ), name='password_change_done'),

    path('create_account_minimal/', views.create_account_minimal, name='create_account_minimal'),
]
