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

## 🚀 Быстрый старт

Для быстрого запуска проекта следуйте инструкции в [QUICK_START.md](QUICK_START.md) (5 минут).

## 📋 Подробная установка

Для полной настройки с интеграцией n8n и всеми функциями следуйте подробной инструкции в [DEPLOYMENT.md](DEPLOYMENT.md).

### Краткий обзор установки:

#### 1. Клонирование репозитория
```bash
git clone https://github.com/zavet-g/complaint-system
cd complaint-system
```

#### 2. Быстрый запуск (рекомендуется)
```bash
chmod +x run.sh
./run.sh
```

#### 3. Настройка API ключей
Скрипт создаст файл `.env`. Отредактируйте его и добавьте ваши API ключи:

```env
SENTIMENT_API_KEY=your_sentiment_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SPAM_API_KEY=your_spam_api_key_here
```

#### 4. Получение API ключей

**Sentiment Analysis API (APILayer)**
- Зарегистрируйтесь на [APILayer](https://apilayer.com/)
- Подпишитесь на [Sentiment Analysis API](https://apilayer.com/marketplace/sentiment-analysis-api)
- Получите API ключ (100 бесплатных запросов/месяц)

**OpenAI API**
- Зарегистрируйтесь на [OpenAI](https://openai.com/)
- Получите API ключ в разделе [API Keys](https://platform.openai.com/api-keys)

**Spam Check API (API Ninjas)**
- Зарегистрируйтесь на [API Ninjas](https://api-ninjas.com/)
- Получите API ключ (50 запросов/день)

#### 5. Запуск приложения

**Быстрый запуск (рекомендуется)**
```bash
./run.sh
```

**Ручной запуск**
```bash
python main.py
```

**Запуск через Docker**
```bash
docker-compose up --build
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

### Telegram уведомления
```bash
# Тестовое уведомление
curl -X POST "http://localhost:8000/telegram/test/"

# Ежедневный отчет
curl -X POST "http://localhost:8000/telegram/daily-report/"
```

### Google Sheets интеграция
```bash
# Настройка заголовков
curl -X POST "http://localhost:8000/sheets/setup/"

# Получение сводки
curl "http://localhost:8000/sheets/summary/"

# Экспорт всех жалоб
curl -X POST "http://localhost:8000/sheets/export/"
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

## 📁 Структура проекта

```
complaint-system/
├── 📁 app/                     # Основное приложение
│   ├── config.py              # Конфигурация приложения
│   ├── models/                # Модели данных
│   ├── routes/                # API маршруты
│   ├── services/              # Бизнес-логика
│   └── utils/                 # Утилиты
├── 📁 tests/                  # Тесты
│   ├── 📁 api/               # API тесты
│   │   └── test_api.py       # Тесты API endpoints
│   ├── 📁 integration/       # Интеграционные тесты
│   │   └── test_integration.py
│   ├── 📁 unit/              # Модульные тесты
│   │   ├── test_telegram.py  # Тесты Telegram
│   │   ├── test_google_sheets.py
│   │   └── test_sheets.py
│   ├── conftest.py           # Конфигурация pytest
│   └── run_all_tests.py      # Запуск всех тестов
├── 📁 docs/                  # Документация
├── main.py                   # Точка входа FastAPI
├── database.py               # Модели базы данных
├── models.py                 # Pydantic модели
├── services.py               # Сервисы для внешних API
├── requirements.txt          # Зависимости Python
├── env.example               # Пример переменных окружения
├── run.sh                    # Скрипт быстрого запуска
├── docker-compose.yml        # Docker Compose
├── Dockerfile                # Docker образ
├── n8n_workflow.json         # Workflow для n8n
├── 📄 *.md                   # Документация
├── .gitignore               # Исключения Git
└── complaints.db            # SQLite БД
```

## 🧪 Тестирование

### Запуск всех тестов
```bash
python tests/run_all_tests.py
```

### Запуск отдельных тестов
```bash
# API тесты
python tests/api/test_api.py

# Интеграционные тесты
python tests/integration/test_integration.py

# Модульные тесты
python tests/unit/test_telegram.py
python tests/unit/test_google_sheets.py
```

### Тестирование с pytest
```bash
# Установка pytest
pip install pytest

# Запуск всех тестов
pytest tests/

# Запуск с подробным выводом
pytest tests/ -v

# Запуск конкретного теста
pytest tests/api/test_api.py::test_create_complaint
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