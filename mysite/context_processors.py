from django.urls import resolve, reverse
from django.urls.exceptions import NoReverseMatch

def generate_navigation(request):
    # Шапка глобальной навигации (дополнена стартовой страницей)
    # 'Стартовая страница' ведёт на '/', проверяем её активность через request.path
    services = [
        {
            'name': 'Стартовая страница',
            'url': '/',
            'active': request.path == '/'
        }
    ]

    # Остальные пункты глобального меню
    namespace_dict = {
        'account': 'Аккаунт',
        'scheduler': 'Расписание',
    }

    if request.user.is_authenticated and request.user.is_staff:
        namespace_dict['administration'] = 'Администрирование'


    # Формируем пункты глобальной навигации (services_nav)
    for ns, title in namespace_dict.items():
        services.append({
            'name': title,
            'url': f'/{ns}/',
            'active': request.path.startswith(f'/{ns}/')
        })

    # Уточняем, какой namespace у текущего URL (или None, если мы на корневом)
    current_ns = request.resolver_match.namespace if request.resolver_match else None

    # Заранее готовим пустой список для локальной навигации
    local_nav = []

    # Словарь, в котором для каждого неймспейса перечислены маршруты локального меню
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

    # Если namespace есть в local_routes, добавляем в локальную навигацию соответствующие ссылки
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
    else:
        # Если мы на стартовой странице (current_ns == None),
        # то в локальную навигацию выводим все пункты из глобальной
        local_nav = services

    return {
        'services_nav': services,  # Глобальное меню
        'local_nav': local_nav,    # Локальное меню
    }
