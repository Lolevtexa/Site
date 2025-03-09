from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EmailScheduleForm, EmailClientConfigForm
from .models import EmailSchedule, EmailClientConfig
from .tasks import send_scheduled_email

@login_required
def schedule_email_view(request):
    """
    Форма для создания записи о запланированном письме.
    При сохранении запись связывается с текущим пользователем и сразу ставится в очередь Celery.
    """
    if request.method == 'POST':
        form = EmailScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            # Запускаем задачу отправки (можно расширить логику для отложенной отправки)
            send_scheduled_email.delay(schedule.pk)
            return redirect('email_schedule_list')
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
            return redirect('configure_email_client')
    else:
        form = EmailClientConfigForm(instance=config)
    return render(request, 'scheduler/configure_email_client.html', {'form': form})
