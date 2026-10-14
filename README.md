# Service Hub

Сайт бытовых услуг: сантехника, электрика, потолки, хендлеры, муж на час, грузчики, такелажники, помощники по хозяйству.

Компания — единая команда разнопрофильных мастеров, которая принимает заказы в одном месте. Сайт также служит рекламной площадкой для соцсетей и агрегаторов.

---

## 🛠 Стек

| Слой | Технология |
|---|---|
| Backend | Python 3.12, Django 5.0 |
| БД | PostgreSQL 16 |
| Очередь | Celery + Redis |
| Frontend | Bootstrap 5, чистый CSS/JS |
| Редактор | CKEditor 5 |
| Аутентификация | кастомный User (email-based), django-axes |
| Зависимости | Poetry 2.x |
| Прод | Docker + Nginx + Gunicorn |

---

## 📂 Структура

```
service_hub/
├── config/                       # настройки Django
│   ├── settings/
│   │   ├── base.py               # общие настройки
│   │   ├── dev.py                # DEBUG=True, debug-toolbar
│   │   └── prod.py               # HSTS, SSL, secure cookies
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── apps/                         # 8 приложений
│   ├── accounts/                 # кастомный User
│   ├── core/                     # SiteSettings, FAQ, PromoCode, Advantage, CallbackRequest
│   ├── services/                 # Category, Service
│   ├── orders/                   # Order, OrderMessage + чат
│   ├── masters/                  # Master, MasterWork
│   ├── reviews/                  # Review
│   ├── blog/                     # Post, Tag
│   └── notifications/            # Celery-задачи
├── templates/                    # HTML-шаблоны
├── static/                       # CSS, JS, изображения
├── fixtures/                     # демо-данные
├── docker/                       # Dockerfile, entrypoint.sh, nginx.conf, certs/
├── deploy/                       # systemd-юниты, nginx.conf, backup.sh
├── docker-compose.yml            # для разработки
├── docker-compose.prod.yml       # для прода
├── .env.example                  # шаблон для локальной разработки
├── .env.prod.example             # шаблон для прода
├── pyproject.toml
├── poetry.lock
└── manage.py
```

---

## 🚀 Быстрый старт (локально)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Maxzonoff/service_hub.git
cd service_hub
```

### 2. Установить зависимости

```bash
poetry install
```

### 3. Настроить окружение

```bash
cp .env.example .env
```

Открыть `.env` и заполнить:
- `SECRET_KEY` — сгенерировать:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- `POSTGRES_*` — параметры локального PostgreSQL
- `EMAIL_*` — можно оставить заглушку (в dev письма пишутся в консоль)

### 4. Создать БД

**Homebrew (macOS):**

```bash
brew install postgresql@16
brew services start postgresql@16
createdb service_hub
```

Затем в psql (под суперпользователем `postgres`):

```sql
CREATE ROLE service_hub WITH LOGIN PASSWORD 'service_hub_pass';
ALTER ROLE service_hub CREATEDB;
ALTER DATABASE service_hub OWNER TO service_hub;
GRANT ALL PRIVILEGES ON DATABASE service_hub TO service_hub;
```

### 5. Миграции + данные

```bash
poetry run python manage.py migrate
poetry run python manage.py loaddata fixtures/*.json
poetry run python manage.py createsuperuser
```

### 6. Запуск

```bash
poetry run python manage.py runserver
```

- Сайт: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/

### 7. Celery (опционально)

**Redis:**

```bash
brew install redis
brew services start redis
```

**В двух отдельных терминалах:**

```bash
poetry run celery -A config worker -l info
poetry run celery -A config beat -l info
```

---

## 🐳 Docker (продакшен)

### Файлы

- `docker/Dockerfile` — образ приложения
- `docker/entrypoint.sh` — миграции + collectstatic при старте
- `docker/nginx/nginx.conf` — конфиг Nginx
- `docker-compose.prod.yml` — 6 сервисов: db, redis, web, celery, celery-beat, nginx
- `.env.prod` — переменные продакшена (создаётся из `.env.prod.example`)

### Запуск

```bash
cp .env.prod.example .env.prod
# Отредактировать .env.prod: SECRET_KEY, домен, SMTP, пароли
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build
```

### Полезные команды

```bash
# Логи веб-сервиса
docker compose -f docker-compose.prod.yml logs -f web

# Django shell
docker compose -f docker-compose.prod.yml exec web python manage.py shell

# Миграции вручную
docker compose -f docker-compose.prod.yml exec web python manage.py migrate

# Загрузка фикстур
docker compose -f docker-compose.prod.yml exec web python manage.py loaddata fixtures/*.json

# Остановка
docker compose -f docker-compose.prod.yml down
```

---

## 🌐 Деплой на Beget VPS (Ubuntu 22.04)

> 📖 **Подробная инструкция** — см. `deploy/README_DEPLOY.md` (когда создадим) или шаги ниже.

### Шаг 1. Подготовка сервера

```bash
ssh root@<IP-сервера>
adduser deploy
usermod -aG sudo deploy
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
su - deploy
```

Обновление системы:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    python3.12 python3.12-venv python3-pip \
    git curl build-essential libpq-dev \
    postgresql postgresql-contrib \
    redis-server nginx \
    certbot python3-certbot-nginx \
    netcat-openbsd
```

Установка Poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
poetry --version
```

### Шаг 2. PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE service_hub;
CREATE USER service_hub WITH PASSWORD 'СИЛЬНЫЙ_ПАРОЛЬ';
ALTER ROLE service_hub SET client_encoding TO 'utf8';
ALTER ROLE service_hub SET default_transaction_isolation TO 'read committed';
ALTER ROLE service_hub SET timezone TO 'Europe/Moscow';
GRANT ALL PRIVILEGES ON DATABASE service_hub TO service_hub;
ALTER DATABASE service_hub OWNER TO service_hub;
\q
```

### Шаг 3. Redis

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
redis-cli ping
# PONG
```

### Шаг 4. Клонировать проект

```bash
cd /home/deploy
git clone https://github.com/Maxzonoff/service_hub.git
cd service_hub
git checkout master
```

### Шаг 5. Настроить `.env.prod`

```bash
cp .env.prod.example .env.prod
nano .env.prod
```

Заполнить: `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `POSTGRES_*`, `EMAIL_*`.

### Шаг 6. Установить зависимости и подготовить данные

```bash
poetry config virtualenvs.in-project true
poetry install --no-root --without dev
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py loaddata fixtures/*.json
python manage.py createsuperuser
deactivate
```

### Шаг 7. Systemd-юниты

Скопировать из `deploy/systemd/` в `/etc/systemd/system/`:

```bash
sudo cp deploy/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable servicehub-web servicehub-celery servicehub-celery-beat
sudo systemctl start servicehub-web servicehub-celery servicehub-celery-beat
sudo systemctl status servicehub-web
```

### Шаг 8. Nginx

```bash
sudo cp deploy/nginx/servicehub.conf /etc/nginx/sites-available/servicehub
sudo ln -s /etc/nginx/sites-available/servicehub /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Шаг 9. SSL (Let's Encrypt)

```bash
sudo certbot --nginx -d servicehub.ru -d www.servicehub.ru
sudo certbot renew --dry-run
```

### Шаг 10. Бэкапы БД (cron)

```bash
chmod +x deploy/backup.sh
crontab -e
```

Добавить:

```
0 3 * * * /home/deploy/service_hub/deploy/backup.sh >> /home/deploy/backups/backup.log 2>&1
```

---

## 🔧 Полезные команды (Django)

```bash
python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser
python manage.py shell
python manage.py loaddata fixtures/*.json
python manage.py collectstatic --noinput
python manage.py check
```

---

## 🧾 Публичные разделы сайта

- `/` — главная (hero, категории, преимущества, отзывы, FAQ)
- `/services/` — каталог услуг
- `/services/<slug>/` — детальная услуга
- `/masters/` — мастера
- `/reviews/` — отзывы + форма
- `/blog/` — SEO-статьи
- `/about/` — о нас
- `/contacts/` — контакты + обратный звонок
- `/orders/create/` — онлайн-заявка
- `/accounts/profile/` — личный кабинет (заказы + чат)
- `/admin/` — админка (дашборд с метриками)

---

## 📞 Контакты

- Email: info@servicehub.ru
- Телефон: +7 (999) 123-45-67

---

## 📄 Лицензия

MIT