from django.urls import path
from .views import (
    schedule_email_view,
    email_schedule_list,
    configure_email_client,
    email_schedule_week_view,
    email_schedule_month_view,
    email_schedule_delete,
    email_schedule_skip_occurrence,
)

app_name = "scheduler"

urlpatterns = [
    path('', email_schedule_list, name='email_schedule_list'),
    path('schedule/', schedule_email_view, name='schedule_email'),
    path('config/', configure_email_client, name='configure_email_client'),
    path('week/', email_schedule_week_view, name='email_schedule_week'),
    path('month/', email_schedule_month_view, name='email_schedule_month'),
    path('delete/<int:pk>/', email_schedule_delete, name='email_schedule_delete'),
    path('skip/<int:pk>/', email_schedule_skip_occurrence, name='email_schedule_skip_occurrence'),
]
