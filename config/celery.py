"""
Конфигурация Celery для проекта Service Hub.

Автоматически находит задачи в приложениях из INSTALLED_APPS
и использует django_celery_beat для периодических задач.
"""

import os

from celery import Celery

# Устанавливаем настройки Django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('service_hub')

# Читаем настройки Celery из settings с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автопоиск задач в файлах tasks.py всех приложений
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Отладочная задача — выводит информацию о запросе."""
    print(f'Request: {self.request!r}')
