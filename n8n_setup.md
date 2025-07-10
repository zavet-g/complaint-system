# 🤖 Настройка n8n Workflow для автоматизации обработки жалоб

## 📋 Обзор

Данный workflow автоматически обрабатывает новые жалобы клиентов каждый час с полной интеграцией всех компонентов системы:
- **Для технических жалоб**: отправляет уведомление в Telegram и закрывает жалобу
- **Для жалоб об оплате**: добавляет запись в Google Sheets и закрывает жалобу
- **Для других жалоб**: логирует и закрывает жалобу

## 🚀 Быстрая настройка (15 минут)

### Шаг 1: Установка n8n

```bash
# Через Docker (рекомендуется)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Или через npm
npm install n8n -g
n8n start

# Или через Docker Compose (если настроен)
docker-compose up n8n
```

### Шаг 2: Предварительная настройка

Убедитесь, что настроены:
- ✅ **Telegram бот** (см. `TELEGRAM_SETUP.md`)
- ✅ **Google Sheets** (см. `GOOGLE_SHEETS_SETUP.md`)
- ✅ **API система** (запущена на localhost:8000)

### Шаг 3: Импорт Workflow

1. **Откройте n8n**: http://localhost:5678
2. **Нажмите "Import from file"**
3. **Выберите файл** `n8n_workflow.json`
4. **Нажмите "Import"**

### Шаг 4: Настройка переменных окружения

В n8n перейдите в **Settings > Variables** и добавьте:

```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id
GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы
API_BASE_URL=http://localhost:8000
```

### Шаг 5: Настройка учетных данных

#### Telegram
1. Перейдите в **Settings > Credentials**
2. Нажмите **"Add Credential"**
3. Выберите **"Telegram"**
4. Введите токен бота

#### Google Sheets
1. Перейдите в **Settings > Credentials**
2. Нажмите **"Add Credential"**
3. Выберите **"Google Sheets"**
4. Загрузите JSON файл сервисного аккаунта

### Шаг 6: Тестирование

```bash
# Создание тестовой жалобы
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Тестовая техническая жалоба для n8n"}'

# Ручной запуск workflow в n8n
# Откройте workflow и нажмите "Execute Workflow"
```

## 🔧 Подробная настройка

### Предварительные требования

#### 1. Настройка Telegram бота

Следуйте подробной инструкции в `TELEGRAM_SETUP.md`:

1. **Создайте бота** через [@BotFather](https://t.me/botfather)
2. **Получите токен** и chat_id
3. **Протестируйте интеграцию**:
   ```bash
   make telegram-test
   ```

#### 2. Настройка Google Sheets

Следуйте подробной инструкции в `GOOGLE_SHEETS_SETUP.md`:

1. **Создайте проект** в Google Cloud Console
2. **Настройте сервисный аккаунт**
3. **Создайте таблицу** и предоставьте доступ
4. **Протестируйте интеграцию**:
   ```bash
   make sheets-test
   ```

#### 3. Запуск API системы

```bash
# Запуск системы
make run

# Проверка здоровья API
make health

# Создание тестовой жалобы
make create-complaint
```

### Импорт Workflow

#### Способ 1: Через веб-интерфейс (рекомендуется)

1. **Откройте n8n**: http://localhost:5678
2. **Нажмите "Import from file"**
3. **Выберите файл** `n8n_workflow.json`
4. **Нажмите "Import"**

#### Способ 2: Через API

```bash
curl -X POST "http://localhost:5678/api/v1/workflows" \
  -H "Content-Type: application/json" \
  -d @n8n_workflow.json
```

#### Способ 3: Через Makefile

```bash
# Если настроен в Makefile
make n8n-import
```

## 📊 Структура Workflow

### Узлы Workflow

#### 1. Schedule Trigger
- **Тип**: Schedule Trigger
- **Интервал**: Каждый час
- **Описание**: Запускает workflow каждый час

#### 2. Get Recent Complaints
- **Тип**: HTTP Request
- **Метод**: GET
- **URL**: `{{ $env.API_BASE_URL }}/complaints/recent/`
- **Query Parameters**:
  - `hours`: `1`
  - `status`: `open`
- **Описание**: Получает новые жалобы за последний час

#### 3. Category Switch
- **Тип**: Switch
- **Правила**:
  - **Правило 1**: `{{ $json.category }}` equals `техническая`
  - **Правило 2**: `{{ $json.category }}` equals `оплата`
  - **По умолчанию**: Другие категории
- **Описание**: Разделяет жалобы по категориям

#### 4. Telegram Notification (для технических жалоб)
- **Тип**: Telegram
- **Операция**: Send Message
- **Chat ID**: `{{ $env.TELEGRAM_CHAT_ID }}`
- **Текст**: 
```
🚨 Новая техническая жалоба!

📝 ID: {{ $json.id }}
📄 Текст: {{ $json.text }}
😊 Тональность: {{ $json.sentiment }}
🏷️ Категория: {{ $json.category }}
📍 IP: {{ $json.ip }}
🕐 Время: {{ $now }}

⚠️ Спам: {{ $json.spam_score > 0.5 ? 'Да' : 'Нет' }}
```

#### 5. Add to Google Sheets (для жалоб об оплате)
- **Тип**: Google Sheets
- **Операция**: Append
- **Document ID**: `{{ $env.GOOGLE_SHEETS_SPREADSHEET_ID }}`
- **Sheet Name**: `Лист1`
- **Columns**:
  - ID: `{{ $json.id }}`
  - Текст: `{{ $json.text }}`
  - Категория: `{{ $json.category }}`
  - Тональность: `{{ $json.sentiment }}`
  - Статус: `{{ $json.status }}`
  - Дата: `{{ $json.timestamp }}`
  - IP: `{{ $json.ip }}`
  - Спам: `{{ $json.spam_score }}`

#### 6. Update Status (для всех жалоб)
- **Тип**: HTTP Request
- **Метод**: PUT
- **URL**: `{{ $env.API_BASE_URL }}/complaints/{{ $json.id }}/`
- **Headers**: `Content-Type: application/json`
- **Body**: `{"status": "closed"}`
- **Описание**: Закрывает обработанную жалобу

### Настройка узлов

#### Schedule Trigger
```json
{
  "type": "n8n-nodes-base.scheduleTrigger",
  "position": [240, 300],
  "parameters": {
    "rule": {
      "interval": [{"field": "hour"}]
    }
  }
}
```

#### HTTP Request - Get Complaints
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "position": [460, 300],
  "parameters": {
    "url": "{{ $env.API_BASE_URL }}/complaints/recent/",
    "method": "GET",
    "queryParameters": {
      "parameters": [
        {
          "name": "hours",
          "value": "1"
        },
        {
          "name": "status",
          "value": "open"
        }
      ]
    }
  }
}
```

#### Switch - Category Filter
```json
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
                "value1": "={{ $json.category }}",
                "operation": "equals",
                "value2": "техническая"
              }
            ]
          }
        },
        {
          "conditions": {
            "string": [
              {
                "value1": "={{ $json.category }}",
                "operation": "equals",
                "value2": "оплата"
              }
            ]
          }
        }
      ]
    }
  }
}
```

## 🧪 Тестирование Workflow

### 1. Ручной запуск
1. **Откройте workflow** в n8n
2. **Нажмите "Execute Workflow"**
3. **Проверьте выполнение** каждого узла
4. **Просмотрите логи** выполнения

### 2. Создание тестовых данных

```bash
# Техническая жалоба (отправит в Telegram)
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Сайт не загружается, постоянно выдает ошибку 500"}'

# Жалоба об оплате (добавит в Google Sheets)
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Не могу оплатить заказ, карта отклоняется"}'

# Другая жалоба (просто закроется)
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Как изменить пароль в личном кабинете?"}'
```

### 3. Проверка результатов

#### Telegram
- Проверьте получение уведомлений в Telegram
- Убедитесь, что формат сообщения корректный

#### Google Sheets
- Откройте вашу Google Sheets таблицу
- Проверьте добавление новых записей
- Убедитесь, что данные корректные

#### API
```bash
# Проверка статуса жалоб
curl "http://localhost:8000/complaints/"

# Проверка недавних жалоб
curl "http://localhost:8000/complaints/recent/?hours=1&status=open"
```

## 🛠️ Устранение неполадок

### Проблема: n8n не запускается

```bash
# Проверка портов
lsof -i :5678

# Проверка Docker
docker ps | grep n8n

# Перезапуск n8n
docker restart n8n
```

### Проблема: Workflow не выполняется

1. **Проверьте переменные окружения** в n8n
2. **Проверьте учетные данные** Telegram и Google Sheets
3. **Проверьте доступность API**:
   ```bash
   curl "http://localhost:8000/health/"
   ```

### Проблема: Telegram не работает

```bash
# Проверка переменных
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# Тест Telegram
make telegram-test
```

### Проблема: Google Sheets не работает

```bash
# Проверка переменных
echo $GOOGLE_SHEETS_SPREADSHEET_ID

# Тест Google Sheets
make sheets-test
```

### Проблема: API недоступен

```bash
# Проверка API
make health

# Перезапуск API
make run
```

## 📊 Мониторинг и логи

### Просмотр логов n8n

```bash
# Docker логи
docker logs n8n

# Логи в реальном времени
docker logs -f n8n

# Поиск ошибок
docker logs n8n | grep -i error
```

### Проверка выполнения workflow

1. **Откройте n8n**: http://localhost:5678
2. **Перейдите в "Executions"**
3. **Просмотрите историю выполнения**
4. **Проверьте детали каждого выполнения**

### Метрики выполнения

```bash
# Количество выполнений
docker logs n8n | grep -c "Workflow executed"

# Количество ошибок
docker logs n8n | grep -c "Error"

# Время выполнения
docker logs n8n | grep "Execution time"
```

## 🔒 Безопасность

### Рекомендации по безопасности

1. **Не публикуйте токены** в публичных репозиториях
2. **Используйте переменные окружения** для конфиденциальных данных
3. **Ограничьте доступ** к n8n только нужным пользователям
4. **Регулярно обновляйте** токены и ключи
5. **Мониторьте логи** на подозрительную активность

### Переменные окружения

```env
# Обязательные
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id
GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы
API_BASE_URL=http://localhost:8000

# Опциональные
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=secure_password
```

## 📚 Дополнительные ресурсы

### Полезные ссылки

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Workflow Examples](https://n8n.io/workflows)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Google Sheets API](https://developers.google.com/sheets/api)

### Команды для разработки

```bash
# Запуск n8n в режиме разработки
docker run -it --rm \
  --name n8n-dev \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  -e N8N_LOG_LEVEL=debug \
  n8nio/n8n

# Экспорт workflow
curl -X GET "http://localhost:5678/api/v1/workflows" \
  -H "Authorization: Bearer YOUR_API_KEY" | jq

# Мониторинг в реальном времени
docker logs -f n8n | grep -E "(executed|error|warning)"
```

## 🎯 Готовые возможности

### ✅ Что работает из коробки:

- Автоматический запуск каждый час
- Получение новых жалоб через API
- Фильтрация по категориям
- Telegram уведомления для технических жалоб
- Google Sheets экспорт для жалоб об оплате
- Автоматическое закрытие обработанных жалоб
- Логирование всех операций
- Обработка ошибок

### 🚀 Готово к production:

- Масштабируемая архитектура
- Обработка ошибок и retry логика
- Мониторинг и логирование
- Безопасное хранение конфиденциальных данных
- Документация и примеры
- Интеграция со всеми компонентами системы 