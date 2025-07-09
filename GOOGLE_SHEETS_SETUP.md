# 📊 Настройка Google Sheets интеграции

## 📋 Обзор

Google Sheets интеграция позволяет автоматически экспортировать жалобы в таблицы Google Sheets для дальнейшего анализа и отчетности.

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
```

### Шаг 8: Установка зависимостей

```bash
pip install gspread google-auth
```

### Шаг 9: Тестирование

```bash
# Настройка заголовков
curl -X POST "http://localhost:8000/sheets/setup/"

# Создание тестовой жалобы
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Тестовая жалоба для Google Sheets"}'
```

## 🔧 Подробная настройка

### Структура Google Sheets

После настройки ваша таблица будет иметь следующие колонки:

| Колонка | Описание |
|---------|----------|
| A | ID жалобы |
| B | Текст жалобы |
| C | Категория |
| D | Тональность |
| E | Статус |
| F | Дата создания |
| G | IP адрес |
| H | Спам |

### Настройка автоматического экспорта

Жалобы автоматически экспортируются в Google Sheets при создании. Для ручного экспорта используйте:

```bash
# Экспорт всех жалоб
curl -X POST "http://localhost:8000/sheets/export/"

# Получение сводки
curl "http://localhost:8000/sheets/summary/"
```

## 🧪 Тестирование интеграции

### Тестовый скрипт

Создайте файл `test_sheets.py`:

```python
#!/usr/bin/env python3
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

async def test_google_sheets():
    base_url = "http://localhost:8000"
    
    print("🧪 Тестирование Google Sheets интеграции")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # 1. Настройка заголовков
        print("1. Настройка заголовков...")
        response = await client.post(f"{base_url}/sheets/setup/")
        if response.status_code == 200:
            print("✅ Заголовки созданы")
        else:
            print(f"❌ Ошибка: {response.text}")
        
        # 2. Создание тестовой жалобы
        print("2. Создание тестовой жалобы...")
        complaint_data = {"text": "Тестовая жалоба для Google Sheets"}
        response = await client.post(
            f"{base_url}/complaints/",
            json=complaint_data
        )
        if response.status_code == 200:
            print("✅ Жалоба создана и экспортирована")
        else:
            print(f"❌ Ошибка: {response.text}")
        
        # 3. Получение сводки
        print("3. Получение сводки...")
        response = await client.get(f"{base_url}/sheets/summary/")
        if response.status_code == 200:
            data = response.json()
            summary = data.get("data", {})
            print(f"✅ Сводка получена: {summary.get('total_complaints', 0)} жалоб")
        else:
            print(f"❌ Ошибка: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_google_sheets())
```

### Ручное тестирование

```bash
# 1. Настройка
curl -X POST "http://localhost:8000/sheets/setup/"

# 2. Создание жалобы
curl -X POST "http://localhost:8000/complaints/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Сайт не работает, не могу войти в аккаунт"}'

# 3. Проверка сводки
curl "http://localhost:8000/sheets/summary/"

# 4. Экспорт всех жалоб
curl -X POST "http://localhost:8000/sheets/export/"
```

## 📊 API Endpoints

### Настройка Google Sheets
```bash
POST /sheets/setup/
```
Создает заголовки таблицы если их нет.

### Получение сводки
```bash
GET /sheets/summary/
```
Возвращает статистику жалоб из Google Sheets.

### Экспорт жалоб
```bash
POST /sheets/export/
```
Экспортирует все жалобы из базы данных в Google Sheets.

## 🔄 Интеграция с n8n

### Workflow для автоматического экспорта

1. **Schedule Trigger** - запуск каждый час
2. **HTTP Request** - получение новых жалоб
3. **Google Sheets** - добавление записей
4. **HTTP Request** - обновление статуса

### Настройка узла Google Sheets в n8n

1. **Добавьте узел Google Sheets**
2. **Выберите операцию**: Append to Sheet
3. **Spreadsheet**: Выберите вашу таблицу
4. **Sheet**: Sheet1
5. **Data**: Настройте маппинг полей

## 🛠️ Устранение неполадок

### Проблема: Ошибка аутентификации

1. **Проверьте файл credentials**:
   ```bash
   ls -la google-credentials.json
   ```

2. **Проверьте переменные окружения**:
   ```bash
   echo $GOOGLE_SHEETS_CREDENTIALS_FILE
   echo $GOOGLE_SHEETS_SPREADSHEET_ID
   ```

3. **Проверьте права доступа**:
   - Убедитесь что сервисный аккаунт добавлен в таблицу
   - Проверьте что у него права "Editor"

### Проблема: Таблица не найдена

1. **Проверьте ID таблицы**:
   - Убедитесь что ID правильный
   - Проверьте что таблица существует

2. **Проверьте доступ**:
   ```bash
   # Тест подключения
   curl "http://localhost:8000/sheets/setup/"
   ```

### Проблема: Зависимости не установлены

```bash
# Установка зависимостей
pip install gspread google-auth

# Проверка установки
python -c "import gspread; print('gspread установлен')"
```

### Проблема: Ошибки в логах

```bash
# Просмотр логов
tail -f logs/app.log

# Поиск ошибок Google Sheets
grep -i "sheets\|google" logs/app.log
```

## 📈 Мониторинг

### Проверка экспорта

```bash
# Получение сводки
curl "http://localhost:8000/sheets/summary/"

# Проверка в Google Sheets
# Откройте вашу таблицу и проверьте новые записи
```

### Автоматические отчеты

Настройте автоматическое создание отчетов:

```bash
# Ежедневный экспорт
curl -X POST "http://localhost:8000/sheets/export/"

# Получение статистики
curl "http://localhost:8000/sheets/summary/"
```

## 🔒 Безопасность

### Рекомендации

1. **Не коммитьте credentials**:
   ```bash
   echo "google-credentials.json" >> .gitignore
   ```

2. **Ограничьте права**:
   - Дайте сервисному аккаунту только необходимые права
   - Используйте отдельную таблицу для тестирования

3. **Мониторьте использование**:
   - Следите за квотами Google Sheets API
   - Проверяйте логи на подозрительную активность

### Переменные окружения

```env
# Обязательные
GOOGLE_SHEETS_CREDENTIALS_FILE=google-credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=ваш_id_таблицы

# Опциональные
GOOGLE_SHEETS_AUTO_EXPORT=true
GOOGLE_SHEETS_BACKUP_ENABLED=true
```

## 🎉 Готово!

После настройки ваша система будет:

- ✅ Автоматически экспортировать жалобы в Google Sheets
- ✅ Создавать красивые отчеты
- ✅ Интегрироваться с n8n
- ✅ Предоставлять статистику

### Проверка работы

1. **Создайте жалобу**:
   ```bash
   curl -X POST "http://localhost:8000/complaints/" \
     -H "Content-Type: application/json" \
     -d '{"text": "Тестовая жалоба"}'
   ```

2. **Проверьте Google Sheets** - новая запись должна появиться автоматически

3. **Получите сводку**:
   ```bash
   curl "http://localhost:8000/sheets/summary/"
   ```

Для получения дополнительной помощи обратитесь к документации Google Sheets API или создайте issue в репозитории проекта. 