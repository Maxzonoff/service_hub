"""
Инициализация проекта.

Загружает Celery-приложение при старте Django,
чтобы декоратор @shared_task работал везде.
"""

from .celery import app as celery_app

__all__ = ('celery_app',)
