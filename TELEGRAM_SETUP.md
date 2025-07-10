# 🤖 Настройка Telegram бота для системы обработки жалоб

## 📋 Обзор

Telegram бот используется для отправки уведомлений о новых жалобах и ежедневных отчетов. Интеграция работает как напрямую через API, так и через n8n workflow. Система поддерживает автоматические уведомления о технических жалобах и ручные отчеты.

## 🚀 Быстрая настройка (5 минут)

### Шаг 1: Создание бота

1. **Откройте Telegram** и найдите [@BotFather](https://t.me/botfather)
2. **Отправьте команду**: `/start`
3. **Отправьте команду**: `/newbot`
4. **Введите имя бота**: `Complaint System Bot`
5. **Введите username**: `complaint_system_bot` (должно заканчиваться на `bot`)
6. **Скопируйте токен**: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### Шаг 2: Получение Chat ID

#### Способ 1: Через @userinfobot (рекомендуется)
1. Найдите [@userinfobot](https://t.me/userinfobot)
2. Отправьте любое сообщение
3. Скопируйте ваш Chat ID (число)

#### Способ 2: Через вашего бота
1. Напишите вашему боту любое сообщение
2. Откройте в браузере: `https://api.telegram.org/botВАШ_ТОКЕН/getUpdates`
3. Найдите в ответе `"chat":{"id":123456789}`

### Шаг 3: Настройка в проекте

Откройте файл `.env` и добавьте:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

### Шаг 4: Тестирование

```bash
# Через Makefile
make telegram-test

# Или напрямую
python tests/unit/test_telegram.py

# Или протестируйте через API
curl -X POST "http://localhost:8000/telegram/test/"
```

## 🔧 Подробная настройка

### Создание бота через BotFather

1. **Найдите @BotFather** в Telegram
2. **Отправьте `/start`**
3. **Отправьте `/newbot`**
4. **Введите имя бота** (например: "Система обработки жалоб")
5. **Введите username** (например: `my_complaint_bot`)
6. **Скопируйте токен** - он выглядит как `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### Настройка команд бота

Отправьте BotFather команду `/setcommands` и выберите вашего бота, затем отправьте:

```
start - Запустить бота
help - Показать справку
status - Статус системы
report - Получить отчет
test - Тестовое уведомление
```

### Получение Chat ID

#### Для личных сообщений:
1. Напишите боту любое сообщение
2. Откройте: `https://api.telegram.org/botВАШ_ТОКЕН/getUpdates`
3. Найдите `"chat":{"id":123456789}`

#### Для групповых чатов:
1. Добавьте бота в группу
2. Напишите в группе любое сообщение
3. Откройте: `https://api.telegram.org/botВАШ_ТОКЕН/getUpdates`
4. Найдите `"chat":{"id":-123456789}` (отрицательный ID для групп)

#### Для каналов:
1. Добавьте бота в канал как администратора
2. Отправьте сообщение в канал
3. Откройте: `https://api.telegram.org/botВАШ_ТОКЕН/getUpdates`
4. Найдите `"chat":{"id":-1001234567890}`

## 🧪 Тестирование интеграции

### Быстрое тестирование

```bash
# Через Makefile
make telegram-test

# Или напрямую
python tests/unit/test_telegram.py
```

Тест проверит:
- ✅ Наличие токена и Chat ID в переменных окружения
- ✅ Подключение к Telegram API
- ✅ Отправку тестового сообщения
- ✅ Корректность формата Chat ID

### API тестирование

```bash
# Тестовое уведомление
curl -X POST "http://localhost:8000/telegram/test/"

# Ежедневный отчет
curl -X POST "http://localhost:8000/telegram/daily-report/"

# Создание жалобы (автоматически отправит уведомление)
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Тестовая жалоба для проверки уведомлений"}'
```

### Ручное тестирование

```bash
# Проверка переменных окружения
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# Проверка подключения к API
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"

# Проверка типа Chat ID (должен быть числом)
python -c "print('Chat ID type:', type(int('$TELEGRAM_CHAT_ID')))"
```

## 📱 Типы уведомлений

### 1. Уведомления о новых жалобах

Отправляются автоматически при создании жалобы:

```
🚨 Новая жалоба #123

📝 Текст: Не приходит SMS-код для подтверждения

🏷️ Категория: техническая
😊 Тональность: negative
📍 IP: 192.168.1.1
🕐 Время: 2024-01-15 14:30:25

⚠️ Спам: Да (score: 0.8)
```

### 2. Ежедневные отчеты

Отправляются по запросу или по расписанию:

```
📊 Ежедневный отчет

📈 Всего жалоб за день: 15
🔴 Открытых жалоб: 8
✅ Обработано: 7

📊 По категориям:
🔧 Технические: 10
💳 Оплата: 3
❓ Другое: 2

😊 По тональности:
😡 Отрицательные: 12
😐 Нейтральные: 2
😊 Положительные: 1

🕐 Отчет сформирован: 2024-01-15 23:59:59
```

### 3. Тестовые уведомления

Для проверки работы интеграции:

```
🧪 Тестовое уведомление

✅ Telegram интеграция работает!
🕐 Время отправки: 2024-01-15 14:30:25
🔧 Система: Complaint System v1.0
```

### 4. Уведомления об ошибках

При проблемах с системой:

```
⚠️ Ошибка системы

❌ Проблема: OpenAI API недоступен
🕐 Время: 2024-01-15 14:30:25
🔧 Действие: Используется fallback категоризация
```

## 🔄 Интеграция с n8n

### Workflow для автоматических уведомлений

1. **Schedule Trigger** - запуск каждый час
2. **HTTP Request** - получение новых жалоб
3. **Switch** - фильтрация по категориям
4. **Telegram** - отправка уведомлений для технических жалоб

### Настройка узла Telegram в n8n

1. **Добавьте узел Telegram**
2. **Выберите операцию**: Send Message
3. **Bot**: Выберите вашего бота
4. **Chat ID**: Введите ваш Chat ID
5. **Text**: Настройте шаблон сообщения

### Пример workflow

```json
{
  "nodes": [
    {
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [240, 300],
      "parameters": {
        "rule": {
          "interval": [{"field": "hour"}]
        }
      }
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "position": [460, 300],
      "parameters": {
        "url": "http://localhost:8000/complaints/recent/?hours=1&status=open",
        "method": "GET"
      }
    },
    {
      "type": "n8n-nodes-base.switch",
      "position": [680, 300],
      "parameters": {
        "rules": {
          "rules": [
            {
              "conditions": {
                "string": [
                  {
                    "value1": "={{$json.category}}",
                    "operation": "equals",
                    "value2": "техническая"
                  }
                ]
              }
            }
          ]
        }
      }
    },
    {
      "type": "n8n-nodes-base.telegram",
      "position": [900, 200],
      "parameters": {
        "operation": "sendMessage",
        "chatId": "{{$env.TELEGRAM_CHAT_ID}}",
        "text": "🚨 Новая техническая жалоба!\n\n📝 {{$json.text}}\n🕐 {{$json.timestamp}}"
      }
    }
  ]
}
```

## 🛠️ Устранение неполадок

### Проблема: Бот не отвечает

```bash
# Проверка токена
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"

# Проверка переменных окружения
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID
```

### Проблема: Сообщения не отправляются

```bash
# Проверка Chat ID
curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "'$TELEGRAM_CHAT_ID'", "text": "Тест"}'

# Проверка типа Chat ID
python -c "print('Chat ID type:', type(int('$TELEGRAM_CHAT_ID')))"
```

### Проблема: Ошибка "Bad Request"

```bash
# Проверка формата токена
echo $TELEGRAM_BOT_TOKEN | grep -E "^[0-9]+:[A-Za-z0-9_-]+$"

# Проверка формата Chat ID
echo $TELEGRAM_CHAT_ID | grep -E "^-?[0-9]+$"
```

### Проблема: Бот заблокирован

1. Напишите боту `/start`
2. Проверьте, что бот не заблокирован
3. Убедитесь, что Chat ID правильный

## 📊 Мониторинг и логи

### Просмотр логов Telegram

```bash
# Поиск Telegram логов
grep -i telegram logs/app.log

# Поиск ошибок Telegram
grep -i "telegram.*error" logs/app.log

# Поиск успешных отправок
grep -i "telegram.*sent" logs/app.log
```

### Проверка статистики

```bash
# Количество отправленных сообщений
grep -c "Telegram message sent" logs/app.log

# Количество ошибок
grep -c "Telegram error" logs/app.log
```

## 🔒 Безопасность

### Рекомендации по безопасности

1. **Не публикуйте токен** в публичных репозиториях
2. **Используйте .env файл** для хранения токена
3. **Регулярно обновляйте токен** при необходимости
4. **Ограничьте доступ** к боту только нужным пользователям
5. **Мониторьте логи** на подозрительную активность

### Переменные окружения

```env
# Обязательные
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id

# Опциональные
TELEGRAM_ENABLED=true
TELEGRAM_NOTIFY_ON_COMPLAINT=true
TELEGRAM_DAILY_REPORT=true
```

## 📚 Дополнительные ресурсы

### Полезные ссылки

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [BotFather Commands](https://core.telegram.org/bots#botfather-commands)
- [Telegram Bot Examples](https://github.com/python-telegram-bot/python-telegram-bot)

### Команды для разработки

```bash
# Тестирование с подробным выводом
python tests/unit/test_telegram.py --verbose

# Проверка конфигурации
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Token:', bool(os.getenv('TELEGRAM_BOT_TOKEN')))
print('Chat ID:', bool(os.getenv('TELEGRAM_CHAT_ID')))
"

# Мониторинг в реальном времени
tail -f logs/app.log | grep -i telegram
```

## 🎯 Готовые возможности

### ✅ Что работает из коробки:

- Автоматические уведомления о новых жалобах
- Ежедневные отчеты по запросу
- Тестовые уведомления для проверки
- Интеграция с n8n workflow
- Обработка ошибок и fallback
- Логирование всех операций
- Полное тестирование интеграции

### 🚀 Готово к production:

- Безопасное хранение токенов
- Валидация входных данных
- Graceful degradation при ошибках
- Мониторинг и логирование
- Документация и примеры 