# ⚡ Быстрый старт - Система обработки жалоб

## 🚀 Самый быстрый способ запуска (5 минут)

### 1. Подготовка (30 секунд)
```bash
# Убедитесь что Python 3.8+ установлен
python3 --version

# Клонируйте репозиторий (если еще не сделали)
git clone https://github.com/zavet-g/complaint-system
cd complaint-system
```

### 2. Первоначальная настройка (1 минута)
```bash
# Создайте виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate

# Установите зависимости
pip install -r requirements.txt

# Сделайте скрипт запуска исполняемым
chmod +x run.sh
```

### 3. Настройка API ключей (3 минуты)
Скопируйте пример конфигурации и отредактируйте:

```bash
cp env.example .env
nano .env  # или любой текстовый редактор
```

Добавьте ваши API ключи:
```env
# Обязательные (для базовой работы)
SENTIMENT_API_KEY=ваш_ключ_apilayer
OPENAI_API_KEY=ваш_ключ_openai  
SPAM_API_KEY=ваш_ключ_api_ninjas

# Опциональные (для полной функциональности)
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id
GOOGLE_SHEETS_CREDENTIALS_FILE=путь_к_файлу_credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы
```

**Где взять ключи:**
- **APILayer**: https://apilayer.com/marketplace/sentiment-analysis-api (100 запросов/месяц бесплатно)
- **OpenAI**: https://platform.openai.com/api-keys
- **API Ninjas**: https://api-ninjas.com/ (50 запросов/день бесплатно)
- **Telegram**: Создайте бота через @BotFather
- **Google Sheets**: Следуйте инструкции в `GOOGLE_SHEETS_SETUP.md`

### 4. Запуск (30 секунд)
```bash
# Быстрый запуск через скрипт
./run.sh

# Или вручную
python main.py
```

## ✅ Проверка работы

### Базовое тестирование
```bash
# Проверка здоровья API
curl http://localhost:8000/health/

# Создание тестовой жалобы
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Сайт не загружается, постоянно выдает ошибку 500"}'

# Получение списка жалоб
curl http://localhost:8000/complaints/
```

### Полное тестирование
```bash
# Запуск всех тестов
python tests/run_all_tests.py

# Или через Makefile
make test
```

## 🌐 Доступные URL

- **API**: http://localhost:8000
- **Документация Swagger**: http://localhost:8000/docs
- **Документация ReDoc**: http://localhost:8000/redoc
- **Проверка здоровья**: http://localhost:8000/health/

## 🧪 Тестирование

### Быстрые команды через Makefile
```bash
# Показать все доступные команды
make help

# Запустить все тесты
make test

# Запустить только API тесты
make test-api

# Создать тестовую жалобу
make create-complaint

# Проверить здоровье API
make health
```

### Ручное тестирование
```bash
# API тесты
python tests/api/test_api.py

# Интеграционные тесты
python tests/integration/test_integration.py

# Модульные тесты
python tests/unit/test_telegram.py
python tests/unit/test_google_sheets.py
```

## 🐳 Альтернативный способ через Docker

```bash
# Настройка
cp env.example .env
nano .env  # добавьте API ключи

# Запуск
docker-compose up --build

# Или через Makefile
make docker-run
```

## 🆘 Если что-то не работает

### Частые проблемы:
1. **Python не найден**: Установите Python 3.8+
2. **Порты заняты**: Измените порты в `.env` или остановите другие сервисы
3. **API ключи не работают**: Проверьте правильность ключей и кредиты
4. **Telegram не работает**: Проверьте токен и chat_id в `.env`
5. **Google Sheets не работает**: Проверьте credentials файл и права доступа

### Диагностика:
```bash
# Проверка зависимостей
pip list

# Проверка переменных окружения
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API keys:', bool(os.getenv('OPENAI_API_KEY')))"

# Проверка логов
tail -f logs/app.log  # если логи включены
```

## 📚 Дополнительная документация

- **Подробная инструкция**: `DEPLOYMENT.md`
- **Настройка Telegram**: `TELEGRAM_SETUP.md`
- **Настройка Google Sheets**: `GOOGLE_SHEETS_SETUP.md`
- **Тестирование**: `TESTING.md`
- **Интеграция с n8n**: `n8n_setup.md`
- **Обзор проекта**: `PROJECT_SUMMARY.md`

## 🎯 Что работает из коробки

- ✅ Создание и управление жалобами
- ✅ AI-категоризация (с fallback на ключевые слова)
- ✅ Анализ тональности (с fallback на ключевые слова)
- ✅ RESTful API с документацией
- ✅ SQLite база данных
- ✅ Telegram уведомления (при настройке)
- ✅ Google Sheets экспорт (при настройке)
- ✅ Полный набор тестов
- ✅ Docker поддержка 