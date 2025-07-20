# 🧪 Тестирование системы обработки жалоб

## 🚀 Быстрое тестирование

### 1. Запуск всех тестов
```bash
# Запустите все тесты одной командой
python tests/run_all_tests.py

# Или через Makefile
make test
```

Этот скрипт проверит:
- ✅ Health check API
- ✅ Создание жалоб с AI-обработкой
- ✅ Telegram уведомления (если настроены)
- ✅ Google Sheets интеграцию (если настроена)
- ✅ Получение списка жалоб
- ✅ Получение недавних жалоб
- ✅ Анализ тональности
- ✅ Категоризацию жалоб

### 2. Тестирование по категориям

#### API тесты
```bash
# Через Makefile
make test-api

# Или напрямую
python tests/api/test_api.py
```

#### Интеграционные тесты
```bash
# Через Makefile
make test-integration

# Или напрямую
python tests/integration/test_integration.py
```

#### Модульные тесты
```bash
# Через Makefile
make test-unit

# Или напрямую
python tests/unit/test_telegram.py
python tests/unit/test_google_sheets.py
```

### 3. Тестирование с pytest
```bash
# Через Makefile
make pytest

# Или напрямую
pytest tests/ -v

# Запуск конкретной категории
pytest tests/api/ -v
pytest tests/unit/ -v
pytest tests/integration/ -v

# Запуск с покрытием кода
pytest tests/ --cov=app --cov-report=html
```

## 🛠️ Удобные команды через Makefile

### Основные команды тестирования
```bash
# Показать все доступные команды
make help

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

# Тест Telegram (если настроен)
make telegram-test

# Тест Google Sheets (если настроен)
make sheets-test
```

### Команды для разработки
```bash
# Установить зависимости
make install

# Запустить сервер
make run

# Запустить в режиме разработки
make dev

# Очистить кэш Python
make clean
```

## 📋 Ручное тестирование

### Проверка здоровья API
```bash
curl "http://localhost:8000/health/"
```

### Создание тестовой жалобы
```bash
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Тестовая жалоба - сайт не работает, постоянно выдает ошибку 500"}'
```

### Получение списка жалоб
```bash
curl "http://localhost:8000/complaints/"
```

### Получение недавних жалоб
```bash
curl "http://localhost:8000/complaints/recent/?hours=1&status=open"
```

### Обновление статуса жалобы
```bash
curl -X PUT "http://localhost:8000/complaints/1/" \
  -H "Content-Type: application/json" \
  -d '{"status": "closed"}'
```

### Тестирование Telegram (если настроен)
```bash
# Тестовое уведомление
curl -X POST "http://localhost:8000/telegram/test/"

# Ежедневный отчет
curl -X POST "http://localhost:8000/telegram/daily-report/"
```

## 🔍 Проверка логов и мониторинг

### Просмотр логов приложения
```bash
# Если логи записываются в файл
tail -f logs/app.log

# Поиск ошибок
grep -i error logs/app.log
grep -i telegram logs/app.log
grep -i openai logs/app.log

# Поиск успешных операций
grep -i "complaint created" logs/app.log
grep -i "sentiment" logs/app.log
```

### Проверка базы данных
```bash
# SQLite
sqlite3 complaints.db ".tables"
sqlite3 complaints.db "SELECT COUNT(*) FROM complaints;"
sqlite3 complaints.db "SELECT * FROM complaints ORDER BY timestamp DESC LIMIT 5;"
sqlite3 complaints.db "SELECT category, COUNT(*) FROM complaints GROUP BY category;"
```

### Проверка переменных окружения
```bash
# Проверка загрузки переменных
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API keys loaded:', bool(os.getenv('OPENAI_API_KEY')))"

# Проверка конкретных переменных
echo $OPENAI_API_KEY
echo $TELEGRAM_BOT_TOKEN
echo $GOOGLE_SHEETS_SPREADSHEET_ID
```

## 🐳 Тестирование в Docker

### Запуск тестов в контейнере
```bash
# Запуск системы через Docker
docker-compose up -d

# Тестирование API
docker exec complaint-api python tests/run_all_tests.py

# Тестирование конкретных компонентов
docker exec complaint-api python tests/api/test_api.py
docker exec complaint-api python tests/unit/test_telegram.py
```

### Просмотр логов Docker
```bash
# Логи API
docker-compose logs complaint-api

# Логи n8n
docker-compose logs n8n

# Все логи
docker-compose logs -f

# Логи с фильтрацией
docker-compose logs complaint-api | grep -i error
```

## 📊 Проверка внешних API

### Проверка Sentiment Analysis API (APILayer)
```bash
curl -H "apikey: ВАШ_API_КЛЮЧ" \
  https://api.apilayer.com/sentiment/analysis \
  -d '{"text": "Я очень доволен сервисом!"}'
```

### Проверка OpenAI API
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer sk-ВАШ_API_КЛЮЧ" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {
        "role": "user",
        "content": "Определи категорию жалобы: Не приходит SMS-код для подтверждения. Варианты: техническая, оплата, другое. Ответ только одним словом."
      }
    ]
  }'
```

### Проверка Spam Check API (API Ninjas)
```bash
curl -H "X-Api-Key: ВАШ_API_КЛЮЧ" \
  "https://api.api-ninjas.com/v1/spamcheck?text=Buy%20now%20cheap%20pills"
```

### Проверка Telegram API
```bash
# Информация о боте
curl "https://api.telegram.org/botВАШ_ТОКЕН/getMe"

# Обновления
curl "https://api.telegram.org/botВАШ_ТОКЕН/getUpdates"

# Отправка тестового сообщения
curl -X POST "https://api.telegram.org/botВАШ_ТОКЕН/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "ВАШ_CHAT_ID", "text": "Тестовое сообщение"}'
```

### Проверка IP API (геолокация)
```bash
curl "http://ip-api.com/json/8.8.8.8"
```

## 🛠️ Устранение неполадок

### Проблема: API недоступен
```bash
# Проверка портов
lsof -i :8000

# Проверка процессов
ps aux | grep python

# Перезапуск
make run
# или
./run.sh
```

### Проблема: База данных недоступна
```bash
# Проверка файла БД
ls -la complaints.db

# Проверка прав доступа
chmod 666 complaints.db

# Пересоздание БД
rm complaints.db
python3 main.py
```

### Проблема: Telegram не работает
```bash
# Проверка переменных окружения
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# Проверка подключения
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"

# Проверка chat_id (должен быть числом)
python -c "print('Chat ID type:', type(int('$TELEGRAM_CHAT_ID')))"
```

### Проблема: OpenAI API не работает
```bash
# Проверка переменной окружения
echo $OPENAI_API_KEY

# Проверка подключения (замените на ваш ключ)
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Проблема: Внешние API недоступны
```bash
# Проверка интернета
ping api.openai.com
ping api.apilayer.com
ping api.api-ninjas.com

# Проверка DNS
nslookup api.openai.com
```

### Проблема: Тесты не проходят
```bash
# Проверка зависимостей
pip list | grep pytest

# Установка недостающих зависимостей
pip install -r requirements.txt

# Запуск тестов с подробным выводом
python tests/run_all_tests.py --verbose

# Запуск конкретного теста
python -m pytest tests/api/test_api.py::test_create_complaint -v
```

## 📈 Метрики и производительность

### Время выполнения тестов
```bash
# Запуск с измерением времени
time python tests/run_all_tests.py

# Запуск pytest с таймингом
pytest tests/ --durations=10
```

### Проверка покрытия кода
```bash
# Установка coverage
pip install coverage

# Запуск с покрытием
coverage run -m pytest tests/
coverage report
coverage html  # создаст html отчет
```

### Нагрузочное тестирование
```bash
# Простое нагрузочное тестирование
for i in {1..10}; do
  curl -X POST "http://localhost:8000/complaints/" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"Тестовая жалоба $i\"}" &
done
wait
```

## 🔧 Настройка тестового окружения

### Создание тестовой конфигурации
```bash
# Копирование конфигурации
cp env.example .env.test

# Редактирование для тестов
nano .env.test

# Запуск с тестовой конфигурацией
ENV_FILE=.env.test python tests/run_all_tests.py
```

### Тестовые данные
```bash
# Создание тестовых жалоб
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Техническая проблема - сайт не загружается"}'

curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Проблема с оплатой - не проходит платеж"}'

curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Общий вопрос - как изменить пароль"}'
```

## 📚 Дополнительные ресурсы

### Документация API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Полезные команды
```bash
# Проверка версий зависимостей
pip freeze

# Обновление зависимостей
pip install -r requirements.txt --upgrade

# Проверка синтаксиса Python
python -m py_compile main.py
python -m py_compile tests/*.py

# Линтинг кода
pip install flake8
flake8 app/ tests/
```

### Интеграция с CI/CD
```bash
# Пример GitHub Actions workflow
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python tests/run_all_tests.py
``` 