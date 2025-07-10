# 📋 Подробная инструкция по развертыванию "Система обработки жалоб клиентов"

## 🎯 Обзор проекта

Полнофункциональная система для обработки жалоб клиентов с современной архитектурой и расширенными возможностями:

### 🚀 Основные возможности
- ✅ **RESTful API** на FastAPI с автоматической документацией
- ✅ **AI-категоризация** жалоб через OpenAI GPT-3.5 (с fallback на ключевые слова)
- ✅ **Анализ тональности** через APILayer (с fallback на ключевые слова)
- ✅ **Проверка на спам** через API Ninjas
- ✅ **Геолокация** по IP через IP API
- ✅ **SQLite база данных** с SQLAlchemy ORM
- ✅ **Telegram уведомления** в реальном времени
- ✅ **Google Sheets интеграция** для экспорта данных
- ✅ **Интеграция с n8n** для автоматизации процессов
- ✅ **Полный набор тестов** (unit, integration, API)
- ✅ **Docker поддержка** для контейнеризации

### 🏗️ Архитектура
```
📁 complaint-system/
├── 📁 app/                     # Основное приложение
│   ├── config.py              # Конфигурация
│   ├── models/                # Модели данных
│   ├── routes/                # API маршруты
│   ├── services/              # Бизнес-логика
│   └── utils/                 # Утилиты
├── 📁 tests/                  # Тесты
│   ├── 📁 api/               # API тесты
│   ├── 📁 integration/       # Интеграционные тесты
│   ├── 📁 unit/              # Модульные тесты
│   └── run_all_tests.py      # Запуск всех тестов
├── main.py                   # Точка входа
├── services.py               # Внешние API сервисы
├── database.py               # Модели БД
├── models.py                 # Pydantic модели
└── 📄 *.md                   # Документация
```

## 🚀 Способ 1: Быстрый запуск (рекомендуется)

### Шаг 1: Подготовка системы
```bash
# Проверьте версию Python (требуется 3.8+)
python3 --version

# Проверьте pip
pip3 --version

# Установите git (если не установлен)
# Ubuntu/Debian: sudo apt install git
# macOS: brew install git
# Windows: https://git-scm.com/download/win
```

### Шаг 2: Клонирование и настройка
```bash
# Клонируйте репозиторий
git clone https://github.com/zavet-g/complaint-system
cd complaint-system

# Создайте виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt

# Сделайте скрипт запуска исполняемым
chmod +x run.sh
```

### Шаг 3: Настройка переменных окружения
```bash
# Скопируйте пример конфигурации
cp env.example .env

# Отредактируйте файл
nano .env  # или code .env, vim .env
```

Добавьте ваши API ключи:
```env
# API Keys (обязательные для базовой работы)
SENTIMENT_API_KEY=ваш_ключ_apilayer_здесь
OPENAI_API_KEY=ваш_ключ_openai_здесь
SPAM_API_KEY=ваш_ключ_api_ninjas_здесь

# Database
DATABASE_URL=sqlite:///./complaints.db

# Server
HOST=0.0.0.0
PORT=8000

# Telegram Bot (опционально)
TELEGRAM_BOT_TOKEN=ваш_токен_бота_здесь
TELEGRAM_CHAT_ID=ваш_chat_id_здесь

# Google Sheets (опционально)
GOOGLE_SHEETS_CREDENTIALS_FILE=path_to_service_account.json
GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы_здесь
GOOGLE_SHEET_NAME=Лист1
```

### Шаг 4: Запуск
```bash
# Быстрый запуск через скрипт
./run.sh

# Или вручную
python main.py

# Или через Makefile
make run
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

### 4. Telegram Bot (опционально)
Следуйте инструкции в `TELEGRAM_SETUP.md`

### 5. Google Sheets (опционально)
Следуйте инструкции в `GOOGLE_SHEETS_SETUP.md`

## 🧪 Тестирование

### Быстрое тестирование
```bash
# Запуск всех тестов
python tests/run_all_tests.py

# Или через Makefile
make test
```

### Детальное тестирование
```bash
# API тесты
make test-api

# Модульные тесты
make test-unit

# Интеграционные тесты
make test-integration

# Тестирование с pytest
make pytest
```

### Ручное тестирование
```bash
# Проверка здоровья API
make health

# Создание тестовой жалобы
make create-complaint

# Получение списка жалоб
make list-complaints

# Тест Telegram
make telegram-test

# Тест Google Sheets
make sheets-test
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
  -d '{"text": "Сайт не загружается, постоянно выдает ошибку 500"}'

# Получение списка жалоб
curl http://localhost:8000/complaints/

# Получение недавних жалоб (для n8n)
curl "http://localhost:8000/complaints/recent/?hours=1&status=open"
```

## 🐳 Способ 2: Запуск через Docker

### Шаг 1: Установка Docker
```bash
# Убедитесь, что Docker установлен
docker --version
docker-compose --version

# Если не установлен:
# Ubuntu/Debian: sudo apt install docker.io docker-compose
# macOS: brew install docker docker-compose
# Windows: https://docs.docker.com/desktop/install/windows/
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

# Или через Makefile
make docker-run
```

### Шаг 4: Проверка работы
```bash
# Проверьте статус контейнеров
docker-compose ps

# Посмотрите логи
docker-compose logs complaint-api
docker-compose logs n8n

# Или через Makefile
make logs
```

## 🔧 Способ 3: Ручная установка

### Шаг 1: Создание виртуального окружения
```bash
# Создайте виртуальное окружение
python3 -m venv .venv

# Активируйте его
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows
```

### Шаг 2: Установка зависимостей
```bash
# Установите зависимости
pip install -r requirements.txt

# Или через Makefile
make install
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

# Или через Makefile
make run
make dev  # режим разработки с автоперезагрузкой
```

## 🤖 Настройка n8n (опционально)

### Шаг 1: Настройка Telegram бота
Следуйте подробной инструкции в `TELEGRAM_SETUP.md`

### Шаг 2: Настройка Google Sheets
Следуйте подробной инструкции в `GOOGLE_SHEETS_SETUP.md`

### Шаг 3: Настройка n8n workflow
Следуйте инструкции в `n8n_setup.md`

## 🛠️ Устранение неполадок

### Проблема: API недоступен
```bash
# Проверка портов
lsof -i :8000

# Проверка процессов
ps aux | grep python

# Перезапуск
make run
```

### Проблема: База данных недоступна
```bash
# Проверка файла БД
ls -la complaints.db

# Проверка прав доступа
chmod 666 complaints.db

# Пересоздание БД
rm complaints.db
python main.py
```

### Проблема: Telegram не работает
```bash
# Проверка переменных окружения
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# Проверка подключения
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
```

### Проблема: Внешние API не работают
```bash
# Проверка интернета
ping api.apilayer.com
ping api.openai.com

# Проверка API ключей
python tests/unit/test_telegram.py
```

### Проблема: Тесты не проходят
```bash
# Проверка зависимостей
pip list | grep pytest

# Установка недостающих зависимостей
pip install -r requirements.txt

# Запуск тестов с подробным выводом
python tests/run_all_tests.py
```

## 📊 Мониторинг и логи

### Просмотр логов
```bash
# Если логи записываются в файл
tail -f logs/app.log

# Поиск ошибок
grep -i error logs/app.log
grep -i telegram logs/app.log

# Docker логи
docker-compose logs -f
```

### Проверка базы данных
```bash
# SQLite
sqlite3 complaints.db ".tables"
sqlite3 complaints.db "SELECT COUNT(*) FROM complaints;"
sqlite3 complaints.db "SELECT * FROM complaints ORDER BY timestamp DESC LIMIT 5;"
```

## 📚 Дополнительная документация

- **Быстрый старт**: `QUICK_START.md`
- **Настройка Telegram**: `TELEGRAM_SETUP.md`
- **Настройка Google Sheets**: `GOOGLE_SHEETS_SETUP.md`
- **Тестирование**: `TESTING.md`
- **Интеграция с n8n**: `n8n_setup.md`
- **Обзор проекта**: `PROJECT_SUMMARY.md`

## 🎯 Следующие шаги

1. **Настройте Telegram бота** для уведомлений
2. **Настройте Google Sheets** для экспорта данных
3. **Создайте n8n workflow** для автоматизации
4. **Настройте мониторинг** и логирование
5. **Добавьте CI/CD** для автоматического тестирования
6. **Настройте production окружение** с PostgreSQL 