"""
Базовые настройки Django для проекта Service Hub.

Содержит общие настройки для всех окружений (dev, prod).
Чувствительные данные читаются из переменных окружения (.env).
"""

from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ─────────────────────────────────────────────
# Безопасность
# ─────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://127.0.0.1:8000,http://localhost:8000',
    cast=Csv(),
)

# ─────────────────────────────────────────────
# Приложения
# ─────────────────────────────────────────────
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'django_ckeditor_5',
    'widget_tweaks',
    'django_celery_beat',
    'axes',
]

LOCAL_APPS = [
    'apps.core',
    'apps.accounts',
    'apps.services',
    'apps.orders',
    'apps.reviews',
    'apps.blog',
    'apps.notifications',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ─────────────────────────────────────────────
# Middleware
# ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# ─────────────────────────────────────────────
# Шаблоны
# ─────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_settings',
            ],
        },
    },
]

# ─────────────────────────────────────────────
# База данных
# ─────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', cast=int),
        'CONN_MAX_AGE': 600,
    }
}

# ─────────────────────────────────────────────
# Аутентификация
# ─────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:profile'
LOGOUT_REDIRECT_URL = 'core:home'

# ─────────────────────────────────────────────
# Локализация
# ─────────────────────────────────────────────
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────
# Статика и медиа
# ─────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────────────────────
# CKEditor 5
# ─────────────────────────────────────────────
CKEDITOR_5_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
CKEDITOR_5_UPLOAD_PATH = 'uploads/'
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading',
            '|',
            'bold',
            'italic',
            'link',
            'bulletedList',
            'numberedList',
            '|',
            'blockQuote',
            'insertTable',
            'uploadImage',
            '|',
            'undo',
            'redo',
        ],
        'height': '400px',
        'width': '100%',
        'language': 'ru',
    },
}

# ─────────────────────────────────────────────
# Email
# ─────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=465, cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Service Hub <noreply@example.com>')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@example.com')

# ─────────────────────────────────────────────
# SMS
# ─────────────────────────────────────────────
SMS_API_KEY = config('SMS_API_KEY', default='')
SMS_SENDER = config('SMS_SENDER', default='ServiceHub')

# ─────────────────────────────────────────────
# Celery
# ─────────────────────────────────────────────
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://redis:6379/1')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://redis:6379/2')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

REDIS_URL = config('REDIS_URL', default='redis://redis:6379/0')

# ─────────────────────────────────────────────
# django-axes
# ─────────────────────────────────────────────
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCKOUT_TEMPLATE = None
AXES_RESET_ON_SUCCESS = True

# ─────────────────────────────────────────────
# Логирование
# ─────────────────────────────────────────────
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '[{asctime}] {levelname} {name} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'root': {'handlers': ['console', 'file'], 'level': 'INFO'},
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False},
        'apps': {'handlers': ['console', 'file'], 'level': 'DEBUG', 'propagate': False},
    },
}

# ─────────────────────────────────────────────
# Бизнес-настройки
# ─────────────────────────────────────────────
SITE_NAME = 'Service Hub'
SITE_DESCRIPTION = (
    'Бытовые услуги в одном месте: сантехника, электрика, потолки, грузчики, муж на час'
)
SITE_URL = 'http://127.0.0.1:8000'
