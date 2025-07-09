#!/usr/bin/env python3
"""
Тестовый скрипт для проверки Google Sheets интеграции
"""

import asyncio
import httpx
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

async def test_google_sheets():
    """Тестирование Google Sheets интеграции"""
    base_url = "http://localhost:8000"
    
    print("🧪 Тестирование Google Sheets интеграции")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # 1. Настройка заголовков
        print("1. Настройка заголовков...")
        try:
            response = await client.post(f"{base_url}/sheets/setup/")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    print("✅ Заголовки созданы")
                else:
                    print(f"❌ Ошибка: {data.get('message')}")
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                print(f"   Ответ: {response.text}")
        except Exception as e:
            print(f"❌ Ошибка настройки: {e}")
        
        # 2. Создание тестовой жалобы
        print("2. Создание тестовой жалобы...")
        try:
            complaint_data = {"text": "Тестовая жалоба для Google Sheets - сайт не работает"}
            response = await client.post(
                f"{base_url}/complaints/",
                json=complaint_data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Жалоба создана: ID {data.get('id')}")
                print(f"   Категория: {data.get('category')}")
                print(f"   Тональность: {data.get('sentiment')}")
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                print(f"   Ответ: {response.text}")
        except Exception as e:
            print(f"❌ Ошибка создания жалобы: {e}")
        
        # 3. Получение сводки
        print("3. Получение сводки...")
        try:
            response = await client.get(f"{base_url}/sheets/summary/")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    summary = data.get("data", {})
                    print(f"✅ Сводка получена:")
                    print(f"   Всего жалоб: {summary.get('total_complaints', 0)}")
                    print(f"   По категориям: {summary.get('by_category', {})}")
                    print(f"   По тональности: {summary.get('by_sentiment', {})}")
                    print(f"   Спам: {summary.get('spam_count', 0)}")
                else:
                    print(f"❌ Ошибка: {data.get('message')}")
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                print(f"   Ответ: {response.text}")
        except Exception as e:
            print(f"❌ Ошибка получения сводки: {e}")
        
        # 4. Экспорт всех жалоб
        print("4. Экспорт всех жалоб...")
        try:
            response = await client.post(f"{base_url}/sheets/export/")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    export_data = data.get("data", {})
                    print(f"✅ Экспорт завершен:")
                    print(f"   Всего жалоб: {export_data.get('total_complaints', 0)}")
                    print(f"   Экспортировано: {export_data.get('exported_count', 0)}")
                else:
                    print(f"❌ Ошибка: {data.get('message')}")
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                print(f"   Ответ: {response.text}")
        except Exception as e:
            print(f"❌ Ошибка экспорта: {e}")

async def check_environment():
    """Проверка переменных окружения"""
    import os
    
    print("🔧 Проверка переменных окружения")
    print("=" * 30)
    
    # Проверка Google Sheets переменных
    credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")
    spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
    
    if not credentials_file or credentials_file == "path_to_service_account.json":
        print("❌ GOOGLE_SHEETS_CREDENTIALS_FILE не настроен")
    else:
        print(f"✅ GOOGLE_SHEETS_CREDENTIALS_FILE: {credentials_file}")
        
        # Проверка существования файла
        if os.path.exists(credentials_file):
            print(f"✅ Файл credentials существует")
        else:
            print(f"❌ Файл credentials не найден: {credentials_file}")
    
    if not spreadsheet_id or spreadsheet_id == "your_spreadsheet_id_here":
        print("❌ GOOGLE_SHEETS_SPREADSHEET_ID не настроен")
    else:
        print(f"✅ GOOGLE_SHEETS_SPREADSHEET_ID: {spreadsheet_id}")
    
    print()

async def test_dependencies():
    """Проверка зависимостей"""
    print("📦 Проверка зависимостей")
    print("=" * 30)
    
    try:
        import gspread
        print("✅ gspread установлен")
    except ImportError:
        print("❌ gspread не установлен")
        print("   Установите: pip install gspread")
    
    try:
        from google.oauth2.service_account import Credentials
        print("✅ google-auth установлен")
    except ImportError:
        print("❌ google-auth не установлен")
        print("   Установите: pip install google-auth")
    
    print()

async def main():
    """Основная функция"""
    print("🚀 Тестирование Google Sheets интеграции")
    print("=" * 60)
    
    # Проверка окружения
    await check_environment()
    
    # Проверка зависимостей
    await test_dependencies()
    
    # Тестирование интеграции
    await test_google_sheets()
    
    print("\n" + "=" * 60)
    print("🎉 Тестирование завершено!")
    print("📊 Проверьте вашу Google Sheets таблицу для подтверждения")

if __name__ == "__main__":
    asyncio.run(main()) 