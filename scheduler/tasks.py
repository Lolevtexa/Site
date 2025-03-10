from celery import shared_task
from django.core.mail import get_connection, EmailMessage
from django.conf import settings
from django.utils.timezone import localtime
from .models import EmailSchedule, EmailClientConfig, EmailScheduleException

@shared_task
def send_scheduled_email(schedule_id):
    try:
        schedule = EmailSchedule.objects.get(pk=schedule_id)
        # Если расписание повторяющееся, проверяем, не помечено ли сегодняшнее выполнение как исключение.
        if schedule.recurrence != 'once':
            today = localtime().date()
            if schedule.exceptions.filter(occurrence_date=today).exists():
                return f"Отправка письма для {today} пропущена (исключение)."
        # Получение индивидуальной конфигурации (если она реализована) или использование глобальных настроек
        try:
            config = EmailClientConfig.objects.get(user=schedule.user)
            connection = get_connection(
                host=config.smtp_host,
                port=config.smtp_port,
                username=config.email_host_user,
                password=config.email_host_password,
                use_tls=config.use_tls,
            )
            from_email = config.email_from if config.email_from else config.email_host_user
        except EmailClientConfig.DoesNotExist:
            # Используем глобальные настройки из settings.py
            connection = get_connection()  # создаёт соединение по умолчанию
            from_email = settings.EMAIL_HOST_USER

        email_msg = EmailMessage(
            subject=schedule.subject,
            body=schedule.message,
            from_email=from_email,
            to=[schedule.recipient],
            connection=connection,
        )
        email_msg.send(fail_silently=False)
        schedule.status = 'sent'
        schedule.save()
        return f"Email sent to {schedule.recipient}"
    except Exception as e:
        schedule.status = f"failed: {str(e)}"
        schedule.save()
        return str(e)
