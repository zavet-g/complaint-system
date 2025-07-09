#!/bin/bash

# Скрипт для запуска системы обработки жалоб клиентов

echo "🚀 Запуск системы обработки жалоб клиентов"
echo "=========================================="

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+"
    exit 1
fi

# Проверка наличия pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip"
    exit 1
fi

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📚 Установка зависимостей..."
pip install -r requirements.txt

# Проверка наличия .env файла
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден. Создаю из примера..."
    cp env.example .env
    echo "📝 Отредактируйте файл .env и добавьте ваши API ключи"
    echo "   Затем запустите скрипт снова"
    exit 1
fi

# Загрузка переменных окружения
export $(cat .env | grep -v '^#' | xargs)

# Проверка API ключей
if [ -z "$SENTIMENT_API_KEY" ] || [ "$SENTIMENT_API_KEY" = "your_sentiment_api_key_here" ]; then
    echo "⚠️  SENTIMENT_API_KEY не настроен в .env файле"
fi

if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "⚠️  OPENAI_API_KEY не настроен в .env файле"
fi

if [ -z "$SPAM_API_KEY" ] || [ "$SPAM_API_KEY" = "your_spam_api_key_here" ]; then
    echo "⚠️  SPAM_API_KEY не настроен в .env файле"
fi

echo "✅ Все проверки пройдены"
echo ""
echo "🌐 Запуск FastAPI сервера..."
echo "   API будет доступен по адресу: http://localhost:8000"
echo "   Документация: http://localhost:8000/docs"
echo ""
echo "Для остановки нажмите Ctrl+C"
echo ""

# Запуск сервера
python main.py 