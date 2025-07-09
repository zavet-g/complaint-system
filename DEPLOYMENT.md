# 📋 Подробная инструкция по запуску проекта "Система обработки жалоб клиентов"

## 🎯 Обзор проекта

Это полнофункциональная система для обработки жалоб клиентов с интеграцией внешних API и автоматизацией через n8n. Система включает:
- RESTful API на FastAPI
- Анализ тональности через APILayer
- Автоматическая категоризация с помощью OpenAI GPT-3.5
- Проверка на спам через API Ninjas
- Геолокация по IP
- SQLite база данных
- Интеграция с n8n для автоматизации
- Telegram уведомления
- Google Sheets интеграция

## 🚀 Способ 1: Быстрый запуск (рекомендуется)

### Шаг 1: Подготовка системы
```bash
# Убедитесь, что у вас установлен Python 3.8+
python3 --version

# Убедитесь, что у вас установлен pip
pip3 --version
```

### Шаг 2: Клонирование и настройка
```bash
# Клонируйте репозиторий (если еще не сделано)
git clone https://github.com/zavet-g/complaint-system
cd complaint-system

# Сделайте скрипт запуска исполняемым
chmod +x run.sh
```

### Шаг 3: Первый запуск
```bash
# Запустите скрипт - он создаст виртуальное окружение и покажет что нужно настроить
./run.sh
```

### Шаг 4: Настройка API ключей
Скрипт создаст файл `.env` из примера. Отредактируйте его:

```bash
nano .env
# или
code .env
```

Замените значения на ваши API ключи:

```env
# API Keys
SENTIMENT_API_KEY=ваш_ключ_apilayer_здесь
OPENAI_API_KEY=ваш_ключ_openai_здесь
SPAM_API_KEY=ваш_ключ_api_ninjas_здесь

# Database
DATABASE_URL=sqlite:///./complaints.db

# Server
HOST=0.0.0.0
PORT=8000

# Telegram Bot (для интеграции с n8n)
TELEGRAM_BOT_TOKEN=ваш_токен_бота_здесь
TELEGRAM_CHAT_ID=ваш_chat_id_здесь

# Google Sheets (для интеграции с n8n)
GOOGLE_SHEETS_CREDENTIALS_FILE=path_to_service_account.json
GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы_здесь
```

### Шаг 5: Повторный запуск
```bash
# Теперь запустите скрипт снова
./run.sh
```

## 🔑 Получение API ключей

### 1. Sentiment Analysis API (APILayer)
1. Зарегистрируйтесь на [APILayer](https://apilayer.com/)
2. Подпишитесь на [Sentiment Analysis API](https://apilayer.com/marketplace/sentiment-analysis-api)
3. Получите API ключ (100 бесплатных запросов/месяц)
4. Скопируйте ключ в `SENTIMENT_API_KEY`

### 2. OpenAI API
1. Зарегистрируйтесь на [OpenAI](https://openai.com/)
2. Перейдите в раздел [API Keys](https://platform.openai.com/api-keys)
3. Создайте новый API ключ
4. Скопируйте ключ в `OPENAI_API_KEY`

### 3. Spam Check API (API Ninjas)
1. Зарегистрируйтесь на [API Ninjas](https://api-ninjas.com/)
2. Получите API ключ (50 запросов/день)
3. Скопируйте ключ в `SPAM_API_KEY`

## 🐳 Способ 2: Запуск через Docker

### Шаг 1: Установка Docker
```bash
# Убедитесь, что Docker установлен
docker --version
docker-compose --version
```

### Шаг 2: Настройка переменных окружения
```bash
# Скопируйте файл с переменными окружения
cp env.example .env

# Отредактируйте .env файл (как описано выше)
nano .env
```

### Шаг 3: Запуск через Docker Compose
```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Или запуск в фоновом режиме
docker-compose up -d
```

### Шаг 4: Проверка работы
```bash
# Проверьте статус контейнеров
docker-compose ps

# Посмотрите логи
docker-compose logs complaint-api
docker-compose logs n8n
```

## 🔧 Способ 3: Ручная установка

### Шаг 1: Создание виртуального окружения
```bash
# Создайте виртуальное окружение
python3 -m venv venv

# Активируйте его
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### Шаг 2: Установка зависимостей
```bash
# Установите зависимости
pip install -r requirements.txt
```

### Шаг 3: Настройка переменных окружения
```bash
# Скопируйте файл с переменными окружения
cp env.example .env

# Отредактируйте .env файл
nano .env
```

### Шаг 4: Запуск приложения
```bash
# Запуск через Python
python main.py

# Или через uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🌐 Проверка работы

### Основные URL:
- **API**: http://localhost:8000
- **Документация Swagger**: http://localhost:8000/docs
- **Документация ReDoc**: http://localhost:8000/redoc
- **Проверка здоровья**: http://localhost:8000/health/

### Тестирование API:
```bash
# Проверка здоровья API
curl http://localhost:8000/health/

# Создание тестовой жалобы
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Не приходит SMS-код для подтверждения"}'

# Получение списка жалоб
curl http://localhost:8000/complaints/
```

## 🤖 Настройка n8n (опционально)

### Шаг 1: Настройка Telegram бота
1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота
3. Добавьте токен в переменную `TELEGRAM_BOT_TOKEN`
4. Получите chat_id и добавьте в `TELEGRAM_CHAT_ID`

### Шаг 2: Настройка Google Sheets
1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите Google Sheets API
3. Создайте сервисный аккаунт и скачайте JSON файл
4. Добавьте путь к файлу в `GOOGLE_SHEETS_CREDENTIALS_FILE`
5. Создайте Google Sheets и добавьте ID в `GOOGLE_SHEETS_SPREADSHEET_ID`

### Шаг 3: Доступ к n8n
- **URL**: http://localhost:5678
- **Логин**: admin
- **Пароль**: admin123

## 🛠️ Устранение неполадок

### Проблема: Python не найден
```bash
# Установите Python 3.8+
# Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS:
brew install python3

# Windows:
# Скачайте с python.org
```

### Проблема: Порты заняты
```bash
# Проверьте какие процессы используют порты
lsof -i :8000
lsof -i :5678

# Остановите процессы или измените порты в .env
```

### Проблема: API ключи не работают
```bash
# Проверьте правильность ключей
# Убедитесь что у вас есть кредиты на API
# Проверьте логи приложения
```

### Проблема: База данных не создается
```bash
# Убедитесь что у вас есть права на запись в директорию
# Проверьте что SQLite установлен
```

## 📁 Структура проекта

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
└── DEPLOYMENT.md           # Эта инструкция
```

## 🎉 Готово!

После выполнения всех шагов ваша система обработки жалоб будет готова к работе. Вы можете:

1. **Отправлять жалобы** через API
2. **Просматривать** обработанные жалобы
3. **Настраивать автоматизацию** через n8n
4. **Получать уведомления** в Telegram
5. **Экспортировать данные** в Google Sheets

Для получения дополнительной помощи обратитесь к документации API по адресу http://localhost:8000/docs 