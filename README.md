# 🚀 Система обработки жалоб клиентов

Современная система для обработки жалоб клиентов с AI-категоризацией, анализом тональности и полной автоматизацией. Проект включает RESTful API, интеграции с внешними сервисами, Telegram уведомления, Google Sheets экспорт и готовую систему тестирования.

## ✨ Возможности

### 🎯 Основные функции
- ✅ **RESTful API** на FastAPI с автоматической документацией
- ✅ **AI-категоризация** жалоб через OpenAI GPT-3.5 (с fallback на ключевые слова)
- ✅ **Анализ тональности** через APILayer (с fallback на ключевые слова для русского языка)
- ✅ **Проверка на спам** через API Ninjas
- ✅ **Геолокация** по IP через IP API
- ✅ **SQLite база данных** с SQLAlchemy ORM

### 🔄 Интеграции и автоматизация
- ✅ **Telegram уведомления** в реальном времени
- ✅ **Google Sheets экспорт** для ведения учета
- ✅ **Интеграция с n8n** для полной автоматизации
- ✅ **Docker поддержка** для контейнеризации

### 🧪 Качество и тестирование
- ✅ **Полный набор тестов** (unit, integration, API)
- ✅ **Makefile** с удобными командами
- ✅ **CI/CD готовность** с pytest
- ✅ **Автоматическая документация** API

## 🚀 Быстрый старт

Для быстрого запуска проекта следуйте инструкцию в [docs/QUICK_START.md](docs/QUICK_START.md).

## 📋 Подробная установка

Для полной настройки с интеграцией n8n и всеми функциями следуйте подробной инструкции в [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

### Краткий обзор установки:

#### 1. Клонирование репозитория
```bash
git clone https://github.com/zavet-g/complaint-system
cd complaint-system
```

#### 2. Первоначальная настройка
```bash
# Создание виртуального окружения
python3 -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Сделайте скрипт запуска исполняемым
chmod +x run.sh
```

#### 3. Настройка API ключей
Скопируйте пример конфигурации и отредактируйте:

```bash
cp env.example .env
nano .env  # или любой текстовый редактор
```

Добавьте ваши API ключи:
```env
# API Keys (обязательные для базовой работы)
SENTIMENT_API_KEY=ваш_ключ_apilayer_здесь
OPENAI_API_KEY=ваш_ключ_openai_здесь
SPAM_API_KEY=ваш_ключ_api_ninjas_здесь

# Опциональные (для полной функциональности)
TELEGRAM_BOT_TOKEN=ваш_токен_бота_здесь
TELEGRAM_CHAT_ID=ваш_chat_id_здесь
GOOGLE_SHEETS_CREDENTIALS_FILE=путь_к_файлу_credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы_здесь
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

**Через Makefile**
```bash
make run
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

## 🧪 Тестирование

Подробное руководство по тестированию смотрите в [docs/TESTING.md](docs/TESTING.md).

### Быстрое тестирование
```bash
# Запуск всех тестов
make test

# Или напрямую
python tests/run_all_tests.py
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

## 📡 API Endpoints

### Создание жалобы
```bash
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Сайт не загружается, постоянно выдает ошибку 500"}'
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

## 📚 Документация API

После запуска приложения документация доступна по адресам:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🔄 Интеграция с n8n

### Настройка Telegram бота

Следуйте подробной инструкции в [docs/TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md):

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен бота и chat_id
3. Добавьте в переменные окружения:
   ```env
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   TELEGRAM_CHAT_ID=ваш_chat_id
   ```

### Настройка Google Sheets

Следуйте подробной инструкции в [docs/GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md):

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)
2. Включите Google Sheets API
3. Создайте сервисный аккаунт и скачайте JSON файл
4. Добавьте в переменные окружения:
   ```env
   GOOGLE_SHEETS_CREDENTIALS_FILE=путь_к_файлу_credentials.json
   GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы
   ```

### Workflow в n8n

Следуйте подробной инструкции в [docs/n8n_setup.md](docs/n8n_setup.md):

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
├── 📁 docs/                   # Документация
│   ├── QUICK_START.md         # Быстрый старт (5 минут)
│   ├── DEPLOYMENT.md          # Подробная установка
│   ├── TESTING.md             # Руководство по тестированию
│   ├── TELEGRAM_SETUP.md      # Настройка Telegram
│   ├── GOOGLE_SHEETS_SETUP.md # Настройка Google Sheets
│   ├── n8n_setup.md           # Настройка n8n
│   └── PROJECT_SUMMARY.md     # Обзор проекта
├── 📁 tests/                  # Тесты
│   ├── 📁 api/               # API тесты
│   │   └── test_api.py       # Тесты API endpoints
│   ├── 📁 integration/       # Интеграционные тесты
│   │   └── test_integration.py
│   ├── 📁 unit/              # Модульные тесты
│   │   ├── test_telegram.py  # Тесты Telegram
│   │   └── test_google_sheets.py
│   └── run_all_tests.py      # Запуск всех тестов
├── main.py                   # Точка входа FastAPI
├── database.py               # Модели базы данных
├── models.py                 # Pydantic модели
├── services.py               # Сервисы для внешних API
├── requirements.txt          # Зависимости Python
├── env.example               # Пример переменных окружения
├── run.sh                    # Скрипт быстрого запуска
├── Makefile                  # Команды для разработки
├── docker-compose.yml        # Docker Compose
├── Dockerfile                # Docker образ
├── n8n_workflow.json         # Workflow для n8n
└── README.md                 # Основная документация
```

## 🛠️ Удобные команды через Makefile

### Основные команды
```bash
# Показать все доступные команды
make help

# Установить зависимости
make install

# Запустить сервер
make run

# Запустить в режиме разработки
make dev

# Очистить кэш Python
make clean
```

### Команды тестирования
```bash
# Запустить все тесты
make test

# Запустить только API тесты
make test-api

# Запустить только модульные тесты
make test-unit

# Запустить только интеграционные тесты
make test-integration

# Запустить тесты с pytest
make pytest
```

### Команды для ручного тестирования
```bash
# Проверить здоровье API
make health

# Создать тестовую жалобу
make create-complaint

# Получить список жалоб
make list-complaints

# Тест Telegram
make telegram-test

# Тест Google Sheets
make sheets-test
```

### Docker команды
```bash
# Запустить через Docker
make docker-run

# Просмотр логов
make logs

# Остановить Docker
make docker-stop
```

## 🔧 Технологический стек

- **FastAPI** - современный веб-фреймворк с автоматической документацией
- **SQLAlchemy 2.0** - современный ORM для работы с базой данных
- **Pydantic** - валидация данных и сериализация
- **httpx** - асинхронные HTTP запросы
- **python-dotenv** - управление переменными окружения
- **pytest** - фреймворк для тестирования
- **Docker** - контейнеризация
- **n8n** - автоматизация процессов

## 📊 Внешние API

- **APILayer Sentiment Analysis** - анализ тональности (100 запросов/месяц бесплатно)
- **OpenAI GPT-3.5 Turbo** - AI-категоризация жалоб
- **API Ninjas Spam Check** - проверка на спам (50 запросов/день бесплатно)
- **IP API** - геолокация по IP (1000 запросов/день бесплатно)
- **Telegram Bot API** - уведомления
- **Google Sheets API** - экспорт данных

## 📚 Документация

### Основные файлы:
- [docs/QUICK_START.md](docs/QUICK_START.md) - быстрый старт 
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - подробная инструкция по развертыванию
- [docs/TESTING.md](docs/TESTING.md) - руководство по тестированию

### Специализированные:
- [docs/TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md) - настройка Telegram бота
- [docs/GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md) - настройка Google Sheets
- [docs/n8n_setup.md](docs/n8n_setup.md) - настройка n8n workflow
- [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - обзор проекта

## 🎯 Готовые возможности

### ✅ Из коробки работает:
- Создание и управление жалобами через REST API
- AI-категоризация с fallback на ключевые слова
- Анализ тональности с поддержкой русского языка
- Telegram уведомления (при настройке)
- Google Sheets экспорт (при настройке)
- Полный набор тестов
- Docker поддержка
- Автоматическая документация API

### 🚀 Готово к production:
- Обработка ошибок и fallback логика
- Валидация данных
- Логирование операций
- Health checks
- Контейнеризация
- Тестирование

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для получения дополнительной информации.

## 🆘 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте документацию в папке `docs/`
2. Посмотрите раздел "Устранение неполадок" в соответствующих MD файлах
3. Создайте issue в репозитории проекта
4. Обратитесь к документации API: http://localhost:8000/docs

## 🎉 Благодарности

- [FastAPI](https://fastapi.tiangolo.com/) - за отличный веб-фреймворк
- [OpenAI](https://openai.com/) - за AI API
- [APILayer](https://apilayer.com/) - за API анализа тональности
- [n8n](https://n8n.io/) - за платформу автоматизации
- [Telegram](https://telegram.org/) - за Bot API
- [Google](https://developers.google.com/sheets) - за Sheets API 