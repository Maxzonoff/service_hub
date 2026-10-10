cat > README.md << 'EOF'
# Service Hub

Сайт бытовых услуг: сантехника, электрика, потолки, хендлеры, муж на час, грузчики, такелажники.

## Стек

- Python 3.12+, Django 5.x, PostgreSQL 16
- Celery + Redis
- Bootstrap 5, чистый CSS/JS
- Docker, Gunicorn, Nginx
- Poetry 2.x

## Быстрый старт (dev)

```bash
git clone <repo>
cd service_hub
cp .env.example .env
poetry install
docker compose up -d db redis
poetry run python manage.py migrate
poetry run python manage.py runserver