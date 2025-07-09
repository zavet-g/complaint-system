# Система обработки жалоб клиентов

Полнофункциональная система для обработки жалоб клиентов с интеграцией внешних API и автоматизацией через n8n.

## Возможности

- ✅ Прием и обработка жалоб клиентов
- ✅ Анализ тональности через APILayer
- ✅ Автоматическая категоризация с помощью OpenAI GPT-3.5
- ✅ Проверка на спам через API Ninjas
- ✅ Геолокация по IP через IP API
- ✅ RESTful API на FastAPI
- ✅ SQLite база данных
- ✅ Интеграция с n8n для автоматизации
- ✅ Telegram уведомления
- ✅ Google Sheets интеграция

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd complaint-system
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Скопируйте файл `env.example` в `.env` и заполните необходимые переменные:

```bash
cp env.example .env
```

Отредактируйте `.env` файл:

```env
# API Keys
SENTIMENT_API_KEY=your_sentiment_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SPAM_API_KEY=your_spam_api_key_here

# Database
DATABASE_URL=sqlite:///./complaints.db

# Server
HOST=0.0.0.0
PORT=8000

# Telegram Bot (for n8n integration)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Google Sheets (for n8n integration)
GOOGLE_SHEETS_CREDENTIALS_FILE=path_to_service_account.json
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
```

### 5. Получение API ключей

#### Sentiment Analysis API (APILayer)
1. Зарегистрируйтесь на [APILayer](https://apilayer.com/)
2. Подпишитесь на [Sentiment Analysis API](https://apilayer.com/marketplace/sentiment-analysis-api)
3. Получите API ключ (100 бесплатных запросов/месяц)

#### OpenAI API
1. Зарегистрируйтесь на [OpenAI](https://openai.com/)
2. Получите API ключ в разделе API Keys

#### Spam Check API (API Ninjas)
1. Зарегистрируйтесь на [API Ninjas](https://api-ninjas.com/)
2. Получите API ключ (50 запросов/день)

### 6. Запуск приложения

#### Быстрый запуск (рекомендуется)
```bash
./run.sh
```

#### Ручной запуск
```bash
python main.py
```

Или с помощью uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Запуск через Docker
```bash
# Сборка и запуск
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d
```

Приложение будет доступно по адресу: http://localhost:8000

## API Endpoints

### Создание жалобы
```bash
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Не приходит SMS-код для подтверждения"}'
```

### Получение списка жалоб
```bash
curl "http://localhost:8000/complaints/"
```

### Получение жалоб за последний час (для n8n)
```bash
curl "http://localhost:8000/complaints/recent/?hours=1&status=open"
```

### Обновление статуса жалобы
```bash
curl -X PUT "http://localhost:8000/complaints/1/" \
  -H "Content-Type: application/json" \
  -d '{"status": "closed"}'
```

### Проверка здоровья API
```bash
curl "http://localhost:8000/health/"
```

## Документация API

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Интеграция с n8n

### Настройка Telegram бота

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Добавьте токен в переменную `TELEGRAM_BOT_TOKEN`
4. Получите chat_id и добавьте в `TELEGRAM_CHAT_ID`

### Настройка Google Sheets

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите Google Sheets API
3. Создайте сервисный аккаунт и скачайте JSON файл
4. Добавьте путь к файлу в `GOOGLE_SHEETS_CREDENTIALS_FILE`
5. Создайте Google Sheets и добавьте ID в `GOOGLE_SHEETS_SPREADSHEET_ID`

### Workflow в n8n

Создайте workflow со следующими узлами:

1. **Schedule Trigger** - запуск каждый час
2. **HTTP Request** - получение новых жалоб
3. **Switch** - разделение по категориям
4. **Telegram** - уведомления для технических жалоб
5. **Google Sheets** - добавление записей для жалоб об оплате
6. **HTTP Request** - обновление статуса на closed

## Структура проекта

```
complaint-system/
├── main.py                 # Основной файл FastAPI приложения
├── database.py             # Модели базы данных
├── models.py               # Pydantic модели
├── services.py             # Сервисы для внешних API
├── requirements.txt        # Зависимости Python
├── env.example             # Пример переменных окружения
├── run.sh                  # Скрипт быстрого запуска
├── test_api.py             # Тестовый скрипт для API
├── docker-compose.yml      # Docker Compose конфигурация
├── Dockerfile              # Docker образ для приложения
├── n8n_workflow.json       # Workflow для n8n
├── n8n_setup.md            # Инструкция по настройке n8n
├── .gitignore              # Исключения для Git
├── README.md               # Документация
└── complaints.db           # SQLite база данных (создается автоматически)
```

## Примеры использования

### Быстрое тестирование

Запустите тестовый скрипт для проверки всех функций API:

```bash
python test_api.py
```

### Создание жалобы через Postman

1. Откройте Postman
2. Создайте POST запрос на `http://localhost:8000/complaints/`
3. Установите Content-Type: application/json
4. Добавьте тело запроса:
```json
{
  "text": "Приложение не работает, не могу войти в аккаунт"
}
```

### Тестирование различных типов жалоб

```bash
# Техническая проблема
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Сайт не загружается, ошибка 500"}'

# Проблема с оплатой
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Списали деньги дважды, нужен возврат"}'

# Общая жалоба
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Плохое обслуживание клиентов"}'
```

## Обработка ошибок

Система обрабатывает следующие ошибки:
- Недоступность внешних API (sentiment = "unknown")
- Ошибки базы данных (HTTP 500)
- Неверные данные (HTTP 422)
- Не найденные ресурсы (HTTP 404)

## Мониторинг

Для мониторинга состояния API используйте эндпоинт `/health/`:

```bash
curl "http://localhost:8000/health/"
```

## Разработка

### Добавление новых API

1. Создайте новый сервис в `services.py`
2. Добавьте необходимые переменные окружения
3. Интегрируйте в основной workflow

### Расширение модели данных

1. Обновите модель в `database.py`
2. Добавьте миграцию базы данных
3. Обновите Pydantic модели в `models.py`

## Лицензия

MIT License

## Поддержка

Для получения поддержки создайте issue в репозитории проекта. 