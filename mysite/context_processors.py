from django.urls import resolve, reverse
from django.urls.exceptions import NoReverseMatch

def generate_navigation(request):
    namespace_dict = {
        'account': 'Аккаунт',
        'administration': 'Администрирование',
        'scheduler': 'Расписание',
    }

    services = []
    for ns, title in namespace_dict.items():
        services.append({'name': title, 'url': f'/{ns}/', 'active': request.path.startswith(f'/{ns}/')})

    current_ns = request.resolver_match.namespace if request.resolver_match else None
    local_nav = []

    local_routes = {
        'account': [
            ('account:profile', 'Профиль'),
            ('account:settings', 'Настройки'),
            ('account:edit_profile', 'Редактировать профиль'),
        ],
        'administration': [
            ('administration:manage_accounts', 'Управление аккаунтами'),
            ('administration:create_account', 'Создать аккаунт'),
            ('administration:create_account_minimal', 'Создать аккаунт (почта)'),
        ],
        'scheduler': [
            ('scheduler:email_schedule_list', 'Запланированные письма'),
            ('scheduler:schedule_email', 'Добавить задачу'),
            ('scheduler:configure_email_client', 'Настроить почтовый клиент'),
        ],
    }

    if current_ns and current_ns in local_routes:
        for route, title in local_routes[current_ns]:
            try:
                url = reverse(route)
                local_nav.append({
                    'name': title,
                    'url': url,
                    'active': request.path == url
                })
            except NoReverseMatch:
                pass

    return {
        'services_nav': services,
        'local_nav': local_nav,
    }
