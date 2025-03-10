from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "administration"

urlpatterns = [
    path('', views.manage_accounts, name='manage_accounts'),
    path('edit_account/<int:user_id>/', views.edit_account, name='edit_account'),
    path('create_account/', views.create_account, name='create_account'),
    path('delete_account/<int:user_id>/', views.delete_account, name='delete_account'),
    path('create_account_minimal/', views.create_account_minimal, name='create_account_minimal'),
]
