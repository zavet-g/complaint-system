# Инструкция по развертыванию системы обработки жалоб

## Варианты развертывания

### 1. Локальное развертывание (для разработки)

#### Требования
- Python 3.8+
- pip
- Git

#### Шаги развертывания

1. **Клонирование репозитория**
```bash
git clone <repository-url>
cd complaint-system
```

2. **Быстрый запуск**
```bash
./run.sh
```

3. **Проверка работы**
```bash
# Тестирование API
python test_api.py

# Проверка документации
open http://localhost:8000/docs
```

### 2. Docker развертывание (для продакшена)

#### Требования
- Docker
- Docker Compose

#### Шаги развертывания

1. **Подготовка файлов**
```bash
# Клонирование репозитория
git clone <repository-url>
cd complaint-system

# Создание .env файла
cp env.example .env
# Отредактируйте .env файл с вашими API ключами
```

2. **Запуск через Docker Compose**
```bash
# Сборка и запуск
docker-compose up --build -d

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f complaint-api
```

3. **Настройка n8n**
```bash
# Откройте n8n в браузере
open http://localhost:5678

# Логин: admin / admin123
# Импортируйте workflow из n8n_workflow.json
```

### 3. Облачное развертывание

#### Heroku

1. **Создание приложения**
```bash
# Установка Heroku CLI
heroku create complaint-system-api

# Добавление переменных окружения
heroku config:set SENTIMENT_API_KEY=your_key
heroku config:set OPENAI_API_KEY=your_key
heroku config:set SPAM_API_KEY=your_key

# Деплой
git push heroku main
```

2. **Настройка базы данных**
```bash
# Добавление PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Обновление DATABASE_URL
heroku config:set DATABASE_URL=$(heroku config:get DATABASE_URL)
```

#### AWS (EC2)

1. **Создание EC2 инстанса**
```bash
# Подключение к инстансу
ssh -i your-key.pem ubuntu@your-instance-ip

# Установка Docker
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu
```

2. **Развертывание приложения**
```bash
# Клонирование репозитория
git clone <repository-url>
cd complaint-system

# Настройка .env
cp env.example .env
nano .env

# Запуск
docker-compose up -d
```

3. **Настройка домена и SSL**
```bash
# Установка Nginx
sudo apt install nginx -y

# Настройка reverse proxy
sudo nano /etc/nginx/sites-available/complaint-system
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/complaint-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# SSL с Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Настройка мониторинга

### 1. Логирование

#### Локальное логирование
```bash
# Просмотр логов приложения
tail -f logs/app.log

# Просмотр логов Docker
docker-compose logs -f complaint-api
```

#### Облачное логирование
```bash
# Heroku
heroku logs --tail

# AWS CloudWatch
aws logs create-log-group --log-group-name complaint-system
aws logs create-log-stream --log-group-name complaint-system --log-stream-name app
```

### 2. Мониторинг здоровья

#### Health Check
```bash
# Проверка состояния API
curl http://localhost:8000/health/

# Автоматическая проверка
while true; do
    curl -f http://localhost:8000/health/ || echo "API недоступен"
    sleep 30
done
```

#### Prometheus + Grafana
```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### 3. Алерты

#### Telegram уведомления
```python
# Добавьте в services.py
async def send_alert(message: str):
    """Отправка алерта в Telegram"""
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        return
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
                json={
                    "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
                    "text": f"🚨 Алерт: {message}"
                }
            )
    except Exception as e:
        print(f"Error sending alert: {e}")
```

## Резервное копирование

### 1. База данных

#### SQLite (локальная)
```bash
# Создание резервной копии
cp complaints.db complaints_backup_$(date +%Y%m%d_%H%M%S).db

# Автоматическое резервное копирование
crontab -e
# Добавьте строку:
0 2 * * * cp /path/to/complaints.db /backup/complaints_$(date +\%Y\%m\%d).db
```

#### PostgreSQL (облачная)
```bash
# Heroku
heroku pg:backups:capture
heroku pg:backups:download

# AWS RDS
aws rds create-db-snapshot \
    --db-instance-identifier complaint-system \
    --db-snapshot-identifier complaint-system-$(date +%Y%m%d)
```

### 2. Конфигурация

```bash
# Резервное копирование конфигурации
tar -czf config_backup_$(date +%Y%m%d).tar.gz .env docker-compose.yml n8n_workflow.json
```

## Масштабирование

### 1. Горизонтальное масштабирование

#### Docker Swarm
```bash
# Инициализация Swarm
docker swarm init

# Развертывание стека
docker stack deploy -c docker-compose.yml complaint-system

# Масштабирование
docker service scale complaint-system_complaint-api=3
```

#### Kubernetes
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: complaint-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: complaint-api
  template:
    metadata:
      labels:
        app: complaint-api
    spec:
      containers:
      - name: complaint-api
        image: complaint-system:latest
        ports:
        - containerPort: 8000
```

### 2. Вертикальное масштабирование

#### Обновление ресурсов
```yaml
# docker-compose.yml
services:
  complaint-api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

## Безопасность

### 1. Переменные окружения

```bash
# Никогда не коммитьте .env файл
echo ".env" >> .gitignore

# Используйте секреты в продакшене
# Heroku
heroku config:set SECRET_KEY=$(openssl rand -hex 32)

# Docker
docker run -e SECRET_KEY=your_secret_key complaint-api
```

### 2. Аутентификация

```python
# Добавьте в main.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != os.getenv("API_TOKEN"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return credentials.credentials

@app.post("/complaints/")
async def create_complaint(
    complaint: ComplaintCreate,
    token: str = Depends(verify_token)
):
    # ... остальной код
```

### 3. Rate Limiting

```python
# Добавьте в main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/complaints/")
@limiter.limit("10/minute")
async def create_complaint(
    complaint: ComplaintCreate,
    request: Request
):
    # ... остальной код
```

## Обновление системы

### 1. Обновление кода

```bash
# Получение обновлений
git pull origin main

# Пересборка Docker образов
docker-compose build --no-cache

# Перезапуск сервисов
docker-compose up -d
```

### 2. Миграции базы данных

```python
# Создайте файл migrations.py
from alembic import command, config
from alembic.config import Config

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

# Добавьте в main.py
@app.on_event("startup")
async def startup_event():
    run_migrations()
```

### 3. Откат изменений

```bash
# Откат к предыдущей версии
git checkout HEAD~1

# Пересборка и перезапуск
docker-compose build --no-cache
docker-compose up -d
```

## Устранение неполадок

### 1. Частые проблемы

#### API недоступен
```bash
# Проверка статуса сервисов
docker-compose ps

# Просмотр логов
docker-compose logs complaint-api

# Проверка портов
netstat -tulpn | grep 8000
```

#### Проблемы с базой данных
```bash
# Проверка подключения к БД
docker exec -it complaint-api python -c "
from database import engine
print(engine.execute('SELECT 1').fetchone())
"

# Резервное копирование и восстановление
docker exec -it complaint-api sqlite3 complaints.db .dump > backup.sql
```

#### Проблемы с внешними API
```bash
# Тестирование API ключей
curl -H "apikey: $SENTIMENT_API_KEY" \
  https://api.apilayer.com/sentiment/analysis \
  -d '{"text": "test"}'
```

### 2. Логи и диагностика

```bash
# Включение debug режима
export DEBUG=True
docker-compose up

# Подробные логи
docker-compose logs -f --tail=100 complaint-api
```

### 3. Мониторинг производительности

```python
# Добавьте в main.py
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
``` 