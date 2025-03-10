import json
import calendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_date
from .forms import EmailScheduleForm, EmailClientConfigForm
from .models import EmailSchedule, EmailClientConfig, EmailScheduleException
from .tasks import send_scheduled_email

@login_required
def configure_email_client(request):
    """
    Позволяет пользователю настроить собственную конфигурацию почтового клиента.
    Если запись уже существует — обновляем, иначе создаём новую.
    """
    try:
        config = request.user.email_config
    except EmailClientConfig.DoesNotExist:
        config = None
    if request.method == 'POST':
        form = EmailClientConfigForm(request.POST, instance=config)
        if form.is_valid():
            email_config = form.save(commit=False)
            email_config.user = request.user
            email_config.save()
            return redirect('scheduler:configure_email_client')
    else:
        form = EmailClientConfigForm(instance=config)
    return render(request, 'scheduler/configure_email_client.html', {'form': form})

@login_required
def schedule_email_view(request):
    if request.method == 'POST':
        form = EmailScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            
            if schedule.recurrence == 'once':
                # Планирование однократной отправки через Celery, с установкой времени выполнения (eta)
                send_scheduled_email.apply_async((schedule.pk,), eta=schedule.scheduled_time)
            else:
                # Создание расписания с использованием django-celery-beat
                # Определяем crontab на основе выбранного режима
                if schedule.recurrence == 'daily':
                    # Ежедневно в указанное время (час и минута из scheduled_time)
                    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
                        minute=schedule.scheduled_time.strftime('%M'),
                        hour=schedule.scheduled_time.strftime('%H'),
                        day_of_week='*',
                        day_of_month='*',
                        month_of_year='*',
                    )
                elif schedule.recurrence == 'weekly':
                    # Еженедельно: учитываем день недели, час и минуту
                    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
                        minute=schedule.scheduled_time.strftime('%M'),
                        hour=schedule.scheduled_time.strftime('%H'),
                        day_of_week=schedule.scheduled_time.strftime('%w'),
                        day_of_month='*',
                        month_of_year='*',
                    )
                elif schedule.recurrence == 'monthly':
                    # Ежемесячно: учитываем день месяца, час и минуту
                    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
                        minute=schedule.scheduled_time.strftime('%M'),
                        hour=schedule.scheduled_time.strftime('%H'),
                        day_of_month=schedule.scheduled_time.strftime('%d'),
                        month_of_year='*',
                        day_of_week='*',
                    )
                # Создаем периодическую задачу, имя формируем уникально
                PeriodicTask.objects.create(
                    crontab=crontab_schedule,
                    name=f"email_schedule_{schedule.pk}_{schedule.created_at.timestamp()}",
                    task='scheduler.tasks.send_scheduled_email',
                    args=json.dumps([schedule.pk]),
                )
            return redirect('scheduler:email_schedule_list')
    else:
        form = EmailScheduleForm()
    return render(request, 'scheduler/schedule_email.html', {'form': form})

@login_required
def email_schedule_list(request):
    """
    Отображает список запланированных писем, принадлежащих текущему пользователю.
    """
    schedules = EmailSchedule.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'scheduler/email_schedule_list.html', {'schedules': schedules})

@login_required
def email_schedule_week_view(request):
    """Отображение запланированных писем на текущую неделю."""
    now = timezone.now()
    # Определяем начало недели (предполагаем, что понедельник — первый день недели)
    start_of_week = now - timezone.timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timezone.timedelta(days=6, hours=23, minutes=59, seconds=59)
    
    scheduled_emails = EmailSchedule.objects.filter(
        user=request.user,
        scheduled_time__range=(start_of_week, end_of_week)
    ).order_by('scheduled_time')
    
    context = {
        'scheduled_emails': scheduled_emails,
        'period': 'неделя',
        'start_date': start_of_week,
        'end_date': end_of_week,
    }
    return render(request, 'scheduler/email_schedule_period.html', context)

@login_required
def email_schedule_month_view(request):
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = calendar.monthrange(now.year, now.month)[1]
    end_of_month = now.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
    scheduled_emails = EmailSchedule.objects.filter(
        user=request.user,
        scheduled_time__range=(start_of_month, end_of_month)
    ).order_by('scheduled_time')
    context = {
        'scheduled_emails': scheduled_emails,
        'period': 'месяц',
        'start_date': start_of_month,
        'end_date': end_of_month,
    }
    return render(request, 'scheduler/email_schedule_period.html', context)

@login_required
def email_schedule_delete(request, pk):
    """Удаляет всю цепочку запланированных писем (если recurring – удаляет и PeriodicTask)."""
    schedule = get_object_or_404(EmailSchedule, pk=pk, user=request.user)
    if schedule.recurrence != 'once':
        periodic_tasks = PeriodicTask.objects.filter(name__startswith=f"email_schedule_{schedule.pk}_")
        periodic_tasks.delete()
    schedule.delete()
    messages.success(request, "Запланированное письмо(а) удалено(ы).")
    return redirect('scheduler:email_schedule_list')

@login_required
def email_schedule_skip_occurrence(request, pk):
    """
    Пропускает (удаляет) конкретное письмо из цепочки повторяющихся писем.
    Ожидается параметр GET 'date' (формат YYYY-MM-DD) – дата пропуска.
    """
    schedule = get_object_or_404(EmailSchedule, pk=pk, user=request.user)
    occurrence_date_str = request.GET.get('date')
    if occurrence_date_str:
        occurrence_date = parse_date(occurrence_date_str)
        if occurrence_date:
            EmailScheduleException.objects.get_or_create(schedule=schedule, occurrence_date=occurrence_date)
            messages.success(request, f"Письмо на {occurrence_date} пропущено.")
        else:
            messages.error(request, "Неверный формат даты.")
    else:
        messages.error(request, "Дата не указана.")
    return redirect('scheduler:email_schedule_list')