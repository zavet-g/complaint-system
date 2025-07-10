# 🧪 Тестирование системы обработки жалоб

## 🚀 Быстрое тестирование

### 1. Запуск всех тестов
```bash
# Запустите все тесты одним командой
python tests/run_all_tests.py
```

Этот скрипт проверит:
- ✅ Health check API
- ✅ Создание жалоб
- ✅ Telegram уведомления
- ✅ Google Sheets интеграцию
- ✅ Получение списка жалоб
- ✅ Получение недавних жалоб
- ✅ Ежедневные отчеты

### 2. Тестирование по категориям

#### API тесты
```bash
python tests/api/test_api.py
```

#### Интеграционные тесты
```bash
python tests/integration/test_integration.py
```

#### Модульные тесты
```bash
# Telegram интеграция
python tests/unit/test_telegram.py

# Google Sheets интеграция
python tests/unit/test_google_sheets.py
python tests/unit/test_sheets.py
```

### 3. Тестирование с pytest
```bash
# Установка pytest
pip install pytest

# Запуск всех тестов
pytest tests/

# Запуск с подробным выводом
pytest tests/ -v

# Запуск конкретной категории
pytest tests/api/ -v
pytest tests/unit/ -v
pytest tests/integration/ -v
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
  -d '{"text": "Тестовая жалоба - сайт не работает"}'
```

### Получение списка жалоб
```bash
curl "http://localhost:8000/complaints/"
```

### Тестирование Telegram
```bash
# Тестовое уведомление
curl -X POST "http://localhost:8000/telegram/test/"

# Ежедневный отчет
curl -X POST "http://localhost:8000/telegram/daily-report/"
```

## 🔍 Проверка логов

### Просмотр логов приложения
```bash
# Если логи записываются в файл
tail -f logs/app.log

# Поиск ошибок
grep -i error logs/app.log
grep -i telegram logs/app.log
```

### Проверка базы данных
```bash
# SQLite (если используется)
sqlite3 complaints.db ".tables"
sqlite3 complaints.db "SELECT COUNT(*) FROM complaints;"
```

## 🐳 Тестирование в Docker

### Запуск тестов в контейнере
```bash
# Запуск системы через Docker
docker-compose up -d

# Тестирование API
docker exec complaint-api python test_integration.py

# Тестирование Telegram
docker exec complaint-api python test_telegram.py
```

### Просмотр логов Docker
```bash
# Логи API
docker-compose logs complaint-api

# Логи n8n
docker-compose logs n8n

# Все логи
docker-compose logs -f
```

## 📊 Проверка внешних API

### Проверка Sentiment Analysis API
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
        "content": "Категоризируй эту жалобу: Не приходит SMS-код"
      }
    ]
  }'
```

### Проверка Spam Check API
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
```

## 🛠️ Устранение неполадок

### Проблема: API недоступен
```bash
# Проверка портов
lsof -i :8000

# Проверка процессов
ps aux | grep python

# Перезапуск
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
python test_telegram.py
```

## 📈 Мониторинг производительности

### Проверка времени ответа
```bash
# Измерение времени ответа
time curl "http://localhost:8000/health/"

# Стресс-тест
for i in {1..10}; do
  curl -X POST "http://localhost:8000/complaints/" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"Тестовая жалоба $i\"}"
done
```

### Проверка использования ресурсов
```bash
# Использование CPU и памяти
top -p $(pgrep -f "python main.py")

# Использование диска
du -sh complaints.db
```

## 🎯 Автоматизированное тестирование

### Запуск всех тестов
```bash
#!/bin/bash
echo "🧪 Запуск всех тестов..."

# Тест интеграции
python test_integration.py

# Тест Telegram
python test_telegram.py

# Тест API
python test_api.py

echo "✅ Все тесты завершены"
```

### CI/CD тестирование
```yaml
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
        run: pip install -r requirements.txt
      - name: Run tests
        run: python test_integration.py
```

## 📝 Отчеты о тестировании

### Создание отчета
```bash
# Запуск тестов с сохранением результатов
python test_integration.py > test_report.txt 2>&1

# Анализ результатов
grep -E "(✅|❌)" test_report.txt
```

### Шаблон отчета
```
Дата тестирования: 2024-01-15
Версия системы: 1.0.0
Тестировщик: Имя

Результаты тестов:
✅ Health check API
✅ Создание жалоб
✅ Telegram уведомления
✅ Получение списка жалоб
✅ Получение недавних жалоб
✅ Ежедневные отчеты

Общий результат: 6/6 тестов пройдено (100%)
```

## 🎉 Готово!

После успешного прохождения всех тестов ваша система готова к работе!

- ✅ API работает корректно
- ✅ База данных функционирует
- ✅ Telegram интеграция настроена
- ✅ Внешние API подключены
- ✅ n8n готов к интеграции

Для получения дополнительной помощи обратитесь к документации или создайте issue в репозитории проекта. 