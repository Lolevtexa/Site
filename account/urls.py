from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # Добавляем страницу смены пароля
    path('password/', auth_views.PasswordChangeView.as_view(
            template_name="account/password_change.html"
        ), name='password_change'),
    path('password/done/', auth_views.PasswordChangeDoneView.as_view(
            template_name="account/password_change_done.html"
        ), name='password_change_done'),
]
