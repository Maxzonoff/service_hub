# ─────────────────────────────────────────────
# Dockerfile — образ Django-приложения для продакшена
# ─────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        gettext \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install "poetry==${POETRY_VERSION}"

# Копируем манифесты Poetry (сначала только их — для кеша слоёв)
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем только prod-зависимости (без dev)
RUN poetry install --no-root --without dev

# Копируем весь проект
COPY . /app/

# Точка входа
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]