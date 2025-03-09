from django.db import models
from django.conf import settings
from django.utils import timezone

class EmailClientConfig(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_config'
    )
    smtp_host = models.CharField(max_length=255, default='smtp.gmail.com')
    smtp_port = models.IntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    email_host_user = models.EmailField()
    email_host_password = models.CharField(max_length=255)
    email_from = models.EmailField(blank=True, null=True,
        help_text="Если не указано, будет использоваться email_host_user")

    def __str__(self):
        return f"Конфигурация для {self.user.username}"

RECURRANCE_CHOICES = [
    ('once', 'Один раз'),
    ('daily', 'Ежедневно'),
    ('weekly', 'Еженедельно'),
    ('monthly', 'Ежемесячно'),
]

class EmailSchedule(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scheduled_emails'
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()
    recipient = models.EmailField()
    scheduled_time = models.DateTimeField(default=timezone.now)
    recurrence = models.CharField(max_length=10, choices=RECURRANCE_CHOICES, default='once')
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.user.username}] {self.subject} -> {self.recipient}"

class EmailScheduleException(models.Model):
    """
    Хранит даты, в которые повторяющееся расписание должно быть пропущено.
    """
    schedule = models.ForeignKey(EmailSchedule, on_delete=models.CASCADE, related_name='exceptions')
    occurrence_date = models.DateField()

    def __str__(self):
        return f"Исключение для {self.schedule} на {self.occurrence_date}"