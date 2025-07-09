# Настройка n8n Workflow для автоматизации обработки жалоб

## Обзор

Данный workflow автоматически обрабатывает новые жалобы клиентов каждый час:
- Для технических жалоб: отправляет уведомление в Telegram и закрывает жалобу
- Для жалоб об оплате: добавляет запись в Google Sheets и закрывает жалобу

## Предварительные требования

### 1. Установка n8n

```bash
# Установка через npm
npm install n8n -g

# Или через Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### 2. Настройка Telegram бота

1. Создайте бота через [@BotFather](https://t.me/botfather):
   ```
   /newbot
   ComplaintBot
   complaint_processing_bot
   ```

2. Получите токен бота и добавьте в переменные окружения n8n:
   ```
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

3. Получите chat_id:
   - Добавьте бота в группу или начните с ним диалог
   - Отправьте сообщение боту
   - Перейдите по ссылке: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Найдите `chat.id` в ответе

4. Добавьте chat_id в переменные окружения:
   ```
   TELEGRAM_CHAT_ID=123456789
   ```

### 3. Настройка Google Sheets

1. Создайте проект в [Google Cloud Console](https://console.cloud.google.com/)

2. Включите Google Sheets API:
   - Перейдите в "APIs & Services" > "Library"
   - Найдите "Google Sheets API" и включите

3. Создайте сервисный аккаунт:
   - Перейдите в "APIs & Services" > "Credentials"
   - Нажмите "Create Credentials" > "Service Account"
   - Заполните форму и создайте аккаунт

4. Скачайте JSON ключ:
   - Нажмите на созданный сервисный аккаунт
   - Перейдите на вкладку "Keys"
   - Нажмите "Add Key" > "Create new key" > "JSON"
   - Сохраните файл

5. Создайте Google Sheets:
   - Создайте новую таблицу
   - Скопируйте ID из URL (между /d/ и /edit)
   - Добавьте в переменные окружения:
   ```
   GOOGLE_SHEETS_SPREADSHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
   ```

## Импорт Workflow

### Способ 1: Через веб-интерфейс

1. Откройте n8n: http://localhost:5678

2. Нажмите "Import from file"

3. Выберите файл `n8n_workflow.json`

4. Нажмите "Import"

### Способ 2: Через API

```bash
curl -X POST "http://localhost:5678/api/v1/workflows" \
  -H "Content-Type: application/json" \
  -d @n8n_workflow.json
```

## Настройка узлов

### 1. Schedule Trigger

- **Тип**: Schedule Trigger
- **Интервал**: Каждый час
- **Настройки**: По умолчанию

### 2. Get Recent Complaints

- **Тип**: HTTP Request
- **Метод**: GET
- **URL**: `http://localhost:8000/complaints/recent/`
- **Query Parameters**:
  - `hours`: `1`
  - `status`: `open`

### 3. Category Switch

- **Тип**: Switch
- **Правила**:
  - **Правило 1**: `{{ $json.category }}` equals `техническая`
  - **Правило 2**: `{{ $json.category }}` equals `оплата`
  - **По умолчанию**: Другие категории

### 4. Telegram Notification

- **Тип**: Telegram
- **Операция**: Send Message
- **Chat ID**: `{{ $env.TELEGRAM_CHAT_ID }}`
- **Текст**: 
```
🚨 Новая техническая жалоба!

ID: {{ $json.id }}
Текст: {{ $json.text }}
Тональность: {{ $json.sentiment }}
Категория: {{ $json.category }}

Время: {{ $now }}
```

### 5. Add to Google Sheets

- **Тип**: Google Sheets
- **Операция**: Append
- **Document ID**: `{{ $env.GOOGLE_SHEETS_SPREADSHEET_ID }}`
- **Sheet Name**: `Complaints`
- **Columns**:
  - Дата: `{{ $now }}`
  - ID: `{{ $json.id }}`
  - Текст: `{{ $json.text }}`
  - Тональность: `{{ $json.sentiment }}`
  - Категория: `{{ $json.category }}`
  - Статус: `open`

### 6. Update Status (Technical)

- **Тип**: HTTP Request
- **Метод**: PUT
- **URL**: `http://localhost:8000/complaints/{{ $json.id }}/`
- **Headers**: `Content-Type: application/json`
- **Body**: `{"status": "closed"}`

### 7. Update Status (Payment)

- **Тип**: HTTP Request
- **Метод**: PUT
- **URL**: `http://localhost:8000/complaints/{{ $json.id }}/`
- **Headers**: `Content-Type: application/json`
- **Body**: `{"status": "closed"}`

## Настройка переменных окружения

В n8n перейдите в Settings > Variables и добавьте:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
```

## Настройка учетных данных

### Telegram
1. Перейдите в Settings > Credentials
2. Нажмите "Add Credential"
3. Выберите "Telegram"
4. Введите токен бота

### Google Sheets
1. Перейдите в Settings > Credentials
2. Нажмите "Add Credential"
3. Выберите "Google Sheets"
4. Загрузите JSON файл сервисного аккаунта

## Тестирование Workflow

### 1. Ручной запуск
1. Откройте workflow в n8n
2. Нажмите "Execute Workflow"
3. Проверьте выполнение каждого узла

### 2. Создание тестовых данных
```bash
# Создайте техническую жалобу
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Сайт не работает, ошибка 500"}'

# Создайте жалобу об оплате
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Списали деньги дважды"}'
```

### 3. Проверка результатов
- Проверьте Telegram на наличие уведомлений
- Проверьте Google Sheets на новые записи
- Проверьте статус жалоб в API

## Мониторинг и логи

### Просмотр логов
1. В n8n перейдите в "Executions"
2. Выберите выполнение workflow
3. Просмотрите детали каждого узла

### Настройка уведомлений об ошибках
1. Добавьте узел "Error Trigger" в workflow
2. Подключите к Telegram для уведомлений об ошибках

## Оптимизация

### Производительность
- Настройте интервал выполнения (например, каждые 30 минут)
- Добавьте фильтрацию по приоритету жалоб
- Используйте batch обработку для множественных жалоб

### Надежность
- Добавьте retry логику для HTTP запросов
- Настройте fallback для недоступных сервисов
- Добавьте мониторинг состояния workflow

## Устранение неполадок

### Частые проблемы

1. **Telegram не отправляет сообщения**:
   - Проверьте токен бота
   - Проверьте chat_id
   - Убедитесь, что бот добавлен в чат

2. **Google Sheets не работает**:
   - Проверьте JSON ключ сервисного аккаунта
   - Убедитесь, что API включен
   - Проверьте права доступа к таблице

3. **API недоступен**:
   - Проверьте, что FastAPI приложение запущено
   - Проверьте URL в узлах HTTP Request
   - Проверьте сетевые настройки

### Логирование
Добавьте узлы "Set" для логирования:
```json
{
  "timestamp": "{{ $now }}",
  "complaint_id": "{{ $json.id }}",
  "action": "processed"
}
```

## Расширение функциональности

### Добавление новых категорий
1. Добавьте новые правила в "Category Switch"
2. Создайте соответствующие узлы обработки
3. Настройте специфичную логику для каждой категории

### Интеграция с другими сервисами
- Slack уведомления
- Email уведомления
- Jira тикеты
- CRM системы

### Аналитика
- Добавьте узлы для сбора статистики
- Интегрируйте с Grafana для визуализации
- Настройте алерты на основе метрик 