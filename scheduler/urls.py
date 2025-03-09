from django.urls import path
from .views import schedule_email_view, email_schedule_list, configure_email_client

urlpatterns = [
    path('schedule/', schedule_email_view, name='schedule_email'),
    path('list/', email_schedule_list, name='email_schedule_list'),
    path('config/', configure_email_client, name='configure_email_client'),
]
