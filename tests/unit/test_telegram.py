#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы Telegram бота
"""

import os
import asyncio
import httpx
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

async def test_telegram_bot():
    """Тестирование Telegram бота"""
    
    # Получаем переменные окружения
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or bot_token == "your_telegram_bot_token_here":
        print("❌ TELEGRAM_BOT_TOKEN не настроен в .env файле")
        return False
    
    if not chat_id or chat_id == "your_chat_id_here":
        print("❌ TELEGRAM_CHAT_ID не настроен в .env файле")
        return False
    
    print(f"🤖 Тестирование Telegram бота...")
    print(f"   Bot Token: {bot_token[:10]}...")
    print(f"   Chat ID: {chat_id}")
    
    # Тестовое сообщение
    test_message = "🧪 Тестовое сообщение от системы обработки жалоб!\n\n✅ Бот работает корректно!"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": test_message,
                    "parse_mode": "HTML"
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    print("✅ Сообщение успешно отправлено!")
                    print(f"   Message ID: {result['result']['message_id']}")
                    return True
                else:
                    print(f"❌ Ошибка API: {result.get('description')}")
                    return False
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                print(f"   Ответ: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Ошибка при отправке сообщения: {e}")
        return False

async def get_bot_info():
    """Получение информации о боте"""
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token or bot_token == "your_telegram_bot_token_here":
        print("❌ TELEGRAM_BOT_TOKEN не настроен")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.telegram.org/bot{bot_token}/getMe",
                timeout=10.0
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    bot_info = result["result"]
                    print("🤖 Информация о боте:")
                    print(f"   Имя: {bot_info['first_name']}")
                    print(f"   Username: @{bot_info['username']}")
                    print(f"   ID: {bot_info['id']}")
                else:
                    print(f"❌ Ошибка получения информации: {result.get('description')}")
            else:
                print(f"❌ HTTP ошибка: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Ошибка при получении информации о боте: {e}")

async def main():
    """Основная функция"""
    
    print("🚀 Тестирование Telegram интеграции")
    print("=" * 40)
    
    # Получаем информацию о боте
    await get_bot_info()
    print()
    
    # Тестируем отправку сообщения
    success = await test_telegram_bot()
    
    print()
    if success:
        print("🎉 Telegram бот настроен и работает!")
        print("   Теперь можно использовать его в n8n workflow")
    else:
        print("⚠️  Проверьте настройки в .env файле")
        print("   Убедитесь что бот создан и токен правильный")

if __name__ == "__main__":
    asyncio.run(main()) 