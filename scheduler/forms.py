from django import forms
from .models import EmailSchedule, EmailClientConfig

class EmailScheduleForm(forms.ModelForm):
    class Meta:
        model = EmailSchedule
        fields = ['subject', 'message', 'recipient', 'scheduled_time']

class EmailClientConfigForm(forms.ModelForm):
    class Meta:
        model = EmailClientConfig
        fields = ['smtp_host', 'smtp_port', 'use_tls', 'email_host_user', 'email_host_password', 'email_from']
