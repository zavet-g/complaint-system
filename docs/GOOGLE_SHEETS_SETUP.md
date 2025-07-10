# 📊 Настройка Google Sheets интеграции для системы обработки жалоб

## 📋 Обзор

Google Sheets интеграция позволяет автоматически экспортировать жалобы в таблицы Google Sheets для дальнейшего анализа, отчетности и интеграции с n8n workflow. Система поддерживает автоматический экспорт при создании жалоб и ручной экспорт по запросу.

## 🚀 Быстрая настройка (10 минут)

### Шаг 1: Создание проекта в Google Cloud

1. **Перейдите в [Google Cloud Console](https://console.cloud.google.com/)**
2. **Создайте новый проект**:
   - Нажмите "Select a project" → "New Project"
   - Название: `Complaint System`
   - Нажмите "Create"

### Шаг 2: Включение Google Sheets API

1. **Перейдите в "APIs & Services" → "Library"**
2. **Найдите "Google Sheets API"**
3. **Нажмите "Enable"**

### Шаг 3: Создание сервисного аккаунта

1. **Перейдите в "APIs & Services" → "Credentials"**
2. **Нажмите "Create Credentials" → "Service Account"**
3. **Заполните форму**:
   - Service account name: `complaint-system-sheets`
   - Service account ID: `complaint-system-sheets`
   - Description: `Service account for complaint system Google Sheets integration`
4. **Нажмите "Create and Continue"**
5. **Пропустите роли** (нажмите "Continue")
6. **Нажмите "Done"**

### Шаг 4: Создание ключа

1. **Найдите созданный сервисный аккаунт** в списке
2. **Нажмите на email** (например: `complaint-system-sheets@project-id.iam.gserviceaccount.com`)
3. **Перейдите на вкладку "Keys"**
4. **Нажмите "Add Key" → "Create new key"**
5. **Выберите "JSON"**
6. **Скачайте файл** и переименуйте в `google-credentials.json`

### Шаг 5: Создание Google Sheets

1. **Откройте [Google Sheets](https://sheets.google.com/)**
2. **Создайте новую таблицу**
3. **Назовите её** (например: "Система обработки жалоб")
4. **Скопируйте ID таблицы** из URL:
   ```
   https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
   ```
   ID: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

### Шаг 6: Предоставление доступа

1. **Откройте вашу Google Sheets**
2. **Нажмите "Share"** (в правом верхнем углу)
3. **Добавьте email сервисного аккаунта** (из JSON файла)
4. **Дайте права "Editor"**
5. **Нажмите "Send"**

### Шаг 7: Настройка в проекте

1. **Скопируйте `google-credentials.json` в корень проекта**
2. **Отредактируйте `.env` файл**:

```env
# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE=google-credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы_здесь
GOOGLE_SHEET_NAME=Лист1
```

### Шаг 8: Установка зависимостей

```bash
# Зависимости уже включены в requirements.txt
pip install -r requirements.txt
```

### Шаг 9: Тестирование

```bash
# Через Makefile
make sheets-test

# Или напрямую
python tests/unit/test_google_sheets.py

# Или через API
curl -X POST "http://localhost:8000/sheets/setup/"
```

## 🔧 Подробная настройка

### Структура Google Sheets

После настройки ваша таблица будет иметь следующие колонки:

| Колонка | Описание | Пример |
|---------|----------|--------|
| A | ID жалобы | 1 |
| B | Текст жалобы | Сайт не загружается |
| C | Категория | техническая |
| D | Тональность | negative |
| E | Статус | open |
| F | Дата создания | 2024-01-15 14:30:25 |
| G | IP адрес | 192.168.1.1 |
| H | Спам score | 0.1 |
| I | Геолокация | Moscow, Russia |

### Настройка автоматического экспорта

Жалобы автоматически экспортируются в Google Sheets при создании. Для ручного экспорта используйте:

```bash
# Экспорт всех жалоб
curl -X POST "http://localhost:8000/sheets/export/"

# Получение сводки
curl "http://localhost:8000/sheets/summary/"

# Настройка заголовков
curl -X POST "http://localhost:8000/sheets/setup/"
```

## 🧪 Тестирование интеграции

### Быстрое тестирование

```bash
# Через Makefile
make sheets-test

# Или напрямую
python tests/unit/test_google_sheets.py
```

Тест проверит:
- ✅ Наличие credentials файла
- ✅ Подключение к Google Sheets API
- ✅ Создание заголовков таблицы
- ✅ Экспорт тестовой жалобы
- ✅ Получение сводки

### API тестирование

```bash
# 1. Настройка заголовков
curl -X POST "http://localhost:8000/sheets/setup/"

# 2. Создание тестовой жалобы
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Сайт не работает, не могу войти в аккаунт"}'

# 3. Проверка сводки
curl "http://localhost:8000/sheets/summary/"

# 4. Экспорт всех жалоб
curl -X POST "http://localhost:8000/sheets/export/"
```

### Ручное тестирование

```bash
# Проверка переменных окружения
echo $GOOGLE_SHEETS_CREDENTIALS_FILE
echo $GOOGLE_SHEETS_SPREADSHEET_ID

# Проверка файла credentials
ls -la google-credentials.json

# Проверка подключения к Google Sheets
python -c "
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

load_dotenv()
creds = Credentials.from_service_account_file(
    os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE'),
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID'))
print('✅ Подключение к Google Sheets успешно')
"
```

## 📊 API Endpoints

### Настройка Google Sheets
```bash
POST /sheets/setup/
```
Создает заголовки таблицы если их нет.

**Ответ:**
```json
{
  "status": "success",
  "message": "Google Sheets headers created successfully",
  "data": {
    "headers": ["ID", "Text", "Category", "Sentiment", "Status", "Timestamp", "IP", "Spam Score", "Location"]
  }
}
```

### Экспорт жалоб
```bash
POST /sheets/export/
```
Экспортирует все жалобы в Google Sheets.

**Ответ:**
```json
{
  "status": "success",
  "message": "Complaints exported successfully",
  "data": {
    "exported_count": 15,
    "total_rows": 16
  }
}
```

### Получение сводки
```bash
GET /sheets/summary/
```
Возвращает сводку по экспортированным жалобам.

**Ответ:**
```json
{
  "status": "success",
  "data": {
    "total_complaints": 15,
    "by_category": {
      "техническая": 10,
      "оплата": 3,
      "другое": 2
    },
    "by_sentiment": {
      "negative": 12,
      "neutral": 2,
      "positive": 1
    },
    "last_export": "2024-01-15 14:30:25"
  }
}
```

## 🔄 Интеграция с n8n

### Workflow для автоматического экспорта

1. **Schedule Trigger** - запуск каждый час
2. **HTTP Request** - получение новых жалоб
3. **Switch** - фильтрация по категориям
4. **Google Sheets** - добавление записей для жалоб об оплате

### Настройка узла Google Sheets в n8n

1. **Добавьте узел Google Sheets**
2. **Выберите операцию**: Append
3. **Spreadsheet**: Выберите вашу таблицу
4. **Sheet**: Выберите лист (обычно "Лист1")
5. **Data**: Настройте маппинг данных

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
                    "value2": "оплата"
                  }
                ]
              }
            }
          ]
        }
      }
    },
    {
      "type": "n8n-nodes-base.googleSheets",
      "position": [900, 200],
      "parameters": {
        "operation": "append",
        "spreadsheetId": "{{$env.GOOGLE_SHEETS_SPREADSHEET_ID}}",
        "sheetName": "Лист1",
        "options": {
          "valueInputOption": "RAW"
        },
        "data": [
          {
            "id": "={{$json.id}}",
            "text": "={{$json.text}}",
            "category": "={{$json.category}}",
            "sentiment": "={{$json.sentiment}}",
            "status": "={{$json.status}}",
            "timestamp": "={{$json.timestamp}}"
          }
        ]
      }
    }
  ]
}
```

## 🛠️ Устранение неполадок

### Проблема: Файл credentials не найден

```bash
# Проверка файла
ls -la google-credentials.json

# Проверка переменной окружения
echo $GOOGLE_SHEETS_CREDENTIALS_FILE

# Проверка прав доступа
chmod 600 google-credentials.json
```

### Проблема: Ошибка доступа к Google Sheets

```bash
# Проверка ID таблицы
echo $GOOGLE_SHEETS_SPREADSHEET_ID

# Проверка email сервисного аккаунта
python -c "
import json
with open('google-credentials.json') as f:
    data = json.load(f)
    print('Service account email:', data['client_email'])
"

# Проверка прав доступа в Google Sheets
# Убедитесь, что email сервисного аккаунта добавлен с правами Editor
```

### Проблема: Ошибка "Invalid credentials"

```bash
# Проверка формата JSON файла
python -c "
import json
with open('google-credentials.json') as f:
    data = json.load(f)
    print('JSON valid:', bool(data))
"

# Проверка обязательных полей
python -c "
import json
with open('google-credentials.json') as f:
    data = json.load(f)
    required = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
    for field in required:
        print(f'{field}:', bool(data.get(field)))
"
```

### Проблема: Таблица не найдена

```bash
# Проверка ID таблицы в URL
# https://docs.google.com/spreadsheets/d/ID_ТАБЛИЦЫ/edit

# Проверка подключения
python -c "
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

load_dotenv()
try:
    creds = Credentials.from_service_account_file(
        os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE'),
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID'))
    print('✅ Таблица найдена:', sheet.title)
except Exception as e:
    print('❌ Ошибка:', e)
"
```

## 📊 Мониторинг и логи

### Просмотр логов Google Sheets

```bash
# Поиск Google Sheets логов
grep -i "google.*sheets" logs/app.log

# Поиск ошибок экспорта
grep -i "sheets.*error" logs/app.log

# Поиск успешных экспортов
grep -i "sheets.*export" logs/app.log
```

### Проверка статистики

```bash
# Количество экспортированных жалоб
grep -c "Google Sheets export" logs/app.log

# Количество ошибок
grep -c "Google Sheets error" logs/app.log
```

## 🔒 Безопасность

### Рекомендации по безопасности

1. **Не публикуйте credentials файл** в публичных репозиториях
2. **Используйте .env файл** для хранения путей
3. **Ограничьте права** сервисного аккаунта только к нужным таблицам
4. **Регулярно ротируйте ключи** при необходимости
5. **Мониторьте логи** на подозрительную активность

### Переменные окружения

```env
# Обязательные
GOOGLE_SHEETS_CREDENTIALS_FILE=google-credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы

# Опциональные
GOOGLE_SHEET_NAME=Лист1
GOOGLE_SHEETS_ENABLED=true
GOOGLE_SHEETS_AUTO_EXPORT=true
```

## 📚 Дополнительные ресурсы

### Полезные ссылки

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Google Cloud Console](https://console.cloud.google.com/)
- [gspread Documentation](https://gspread.readthedocs.io/)
- [Google Auth Documentation](https://google-auth.readthedocs.io/)

### Команды для разработки

```bash
# Тестирование с подробным выводом
python tests/unit/test_google_sheets.py --verbose

# Проверка конфигурации
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Credentials file:', bool(os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')))
print('Spreadsheet ID:', bool(os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')))
"

# Мониторинг в реальном времени
tail -f logs/app.log | grep -i "google.*sheets"
```

## 🎯 Готовые возможности

### ✅ Что работает из коробки:

- Автоматический экспорт жалоб при создании
- Ручной экспорт всех жалоб
- Создание заголовков таблицы
- Получение сводки по экспортированным данным
- Интеграция с n8n workflow
- Обработка ошибок и fallback
- Логирование всех операций
- Полное тестирование интеграции

### 🚀 Готово к production:

- Безопасное хранение credentials
- Валидация входных данных
- Graceful degradation при ошибках
- Мониторинг и логирование
- Документация и примеры
- Поддержка различных форматов данных 