def navpan(request):
    panel = [
        {'title': 'Поток',
         'url_name': 'main',
         'url_path': None,
         'url_query': None,
        },
    ]
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            panel.append({
                'title': "Админ-панель",
                'url_name': 'admin:index',
                'url_path': None,
                'url_query': None,
             })
        panel.append({
            'title': 'Создать пост',
            'url_name': 'create_post',
            'url_path': None,
            'url_query': None,
        })
        panel.append({
            'title': 'Профиль',
            'url_name': 'profile',
            'url_path': request.user.id,
            'url_query': None,
        })
        panel.append({
            'title': 'Выход',
            'url_name': 'logout',
            'url_path': None,
            'url_query': f'next={request.path}',
        })
    else:
        panel.append({
            'title': "Вход",
            'url_name': 'login',
            'url_path': None,
            'url_query': f'next={request.path}',
        })
        panel.append({
            'title': "Регистрация",
            'url_name': 'registration',
            'url_path': None,
            'url_query': f'next={request.path}'
        })
    return panel