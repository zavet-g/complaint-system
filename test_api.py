#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы API системы обработки жалоб
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Тест проверки здоровья API"""
    print("🔍 Тестирование health check...")
    try:
        response = requests.get(f"{BASE_URL}/health/")
        if response.status_code == 200:
            print("✅ Health check успешен")
            print(f"   Ответ: {response.json()}")
        else:
            print(f"❌ Health check неудачен: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка health check: {e}")

def test_create_complaint(text, expected_category=None):
    """Тест создания жалобы"""
    print(f"\n📝 Создание жалобы: {text[:50]}...")
    try:
        data = {"text": text}
        response = requests.post(
            f"{BASE_URL}/complaints/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Жалоба создана успешно")
            print(f"   ID: {result['id']}")
            print(f"   Статус: {result['status']}")
            print(f"   Тональность: {result['sentiment']}")
            print(f"   Категория: {result['category']}")
            
            if expected_category and result['category'] == expected_category:
                print(f"   ✅ Категория определена правильно: {expected_category}")
            elif expected_category:
                print(f"   ⚠️  Ожидалась категория: {expected_category}, получена: {result['category']}")
            
            return result['id']
        else:
            print(f"❌ Ошибка создания жалобы: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Ошибка создания жалобы: {e}")
        return None

def test_get_complaints():
    """Тест получения списка жалоб"""
    print("\n📋 Получение списка жалоб...")
    try:
        response = requests.get(f"{BASE_URL}/complaints/")
        if response.status_code == 200:
            complaints = response.json()
            print(f"✅ Получено жалоб: {len(complaints)}")
            for complaint in complaints[:3]:  # Показываем первые 3
                print(f"   ID: {complaint['id']}, Категория: {complaint['category']}, Статус: {complaint['status']}")
        else:
            print(f"❌ Ошибка получения жалоб: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка получения жалоб: {e}")

def test_get_recent_complaints():
    """Тест получения недавних жалоб"""
    print("\n🕐 Получение недавних жалоб...")
    try:
        response = requests.get(f"{BASE_URL}/complaints/recent/?hours=1&status=open")
        if response.status_code == 200:
            complaints = response.json()
            print(f"✅ Получено недавних жалоб: {len(complaints)}")
            for complaint in complaints:
                print(f"   ID: {complaint['id']}, Категория: {complaint['category']}")
        else:
            print(f"❌ Ошибка получения недавних жалоб: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка получения недавних жалоб: {e}")

def test_update_complaint(complaint_id):
    """Тест обновления жалобы"""
    print(f"\n✏️  Обновление жалобы ID: {complaint_id}...")
    try:
        data = {"status": "closed"}
        response = requests.put(
            f"{BASE_URL}/complaints/{complaint_id}/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Жалоба обновлена успешно")
            print(f"   Новый статус: {result['status']}")
        else:
            print(f"❌ Ошибка обновления жалобы: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка обновления жалобы: {e}")

def test_get_complaint(complaint_id):
    """Тест получения конкретной жалобы"""
    print(f"\n🔍 Получение жалобы ID: {complaint_id}...")
    try:
        response = requests.get(f"{BASE_URL}/complaints/{complaint_id}/")
        if response.status_code == 200:
            complaint = response.json()
            print("✅ Жалоба получена успешно")
            print(f"   Текст: {complaint.get('text', 'N/A')[:100]}...")
            print(f"   Статус: {complaint['status']}")
            print(f"   Тональность: {complaint['sentiment']}")
            print(f"   Категория: {complaint['category']}")
        else:
            print(f"❌ Ошибка получения жалобы: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка получения жалобы: {e}")

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов API системы обработки жалоб")
    print("=" * 50)
    
    # Проверяем доступность API
    test_health_check()
    
    # Тестовые жалобы
    test_complaints = [
        {
            "text": "Сайт не загружается, постоянно выдает ошибку 500. Не могу войти в личный кабинет уже третий день.",
            "expected_category": "техническая"
        },
        {
            "text": "Списали деньги дважды за одну услугу. Нужен немедленный возврат средств на карту.",
            "expected_category": "оплата"
        },
        {
            "text": "Плохое обслуживание клиентов. Операторы грубят и не решают проблемы.",
            "expected_category": "другое"
        },
        {
            "text": "Приложение не работает на iPhone, постоянно вылетает при попытке загрузки фотографий.",
            "expected_category": "техническая"
        },
        {
            "text": "Не приходит SMS-код для подтверждения входа в систему.",
            "expected_category": "техническая"
        }
    ]
    
    created_ids = []
    
    # Создаем тестовые жалобы
    for i, complaint in enumerate(test_complaints, 1):
        print(f"\n--- Тест {i} ---")
        complaint_id = test_create_complaint(
            complaint["text"], 
            complaint["expected_category"]
        )
        if complaint_id:
            created_ids.append(complaint_id)
        time.sleep(1)  # Небольшая пауза между запросами
    
    # Тестируем получение списка жалоб
    test_get_complaints()
    
    # Тестируем получение недавних жалоб
    test_get_recent_complaints()
    
    # Тестируем получение конкретной жалобы
    if created_ids:
        test_get_complaint(created_ids[0])
    
    # Тестируем обновление жалобы
    if created_ids:
        test_update_complaint(created_ids[0])
    
    print("\n" + "=" * 50)
    print("🏁 Тестирование завершено!")
    print(f"📊 Создано тестовых жалоб: {len(created_ids)}")
    print(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 