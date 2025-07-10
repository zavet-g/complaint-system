#!/usr/bin/env python3
"""
Тестовый скрипт для проверки всей интеграции системы
"""

import asyncio
import httpx
import json
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class IntegrationTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.results = {}
    
    async def test_health_check(self):
        """Тестирование проверки здоровья API"""
        print("🏥 Тестирование health check...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/health/")
                if response.status_code == 200:
                    print("✅ Health check работает")
                    self.results["health"] = True
                    return True
                else:
                    print(f"❌ Health check не работает: {response.status_code}")
                    self.results["health"] = False
                    return False
        except Exception as e:
            print(f"❌ Ошибка health check: {e}")
            self.results["health"] = False
            return False
    
    async def test_complaint_creation(self):
        """Тестирование создания жалобы"""
        print("📝 Тестирование создания жалобы...")
        try:
            test_complaint = {
                "text": "Тестовая жалоба для проверки интеграции - сайт не работает"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/complaints/",
                    json=test_complaint,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Жалоба создана: ID {data.get('id')}")
                    print(f"   Категория: {data.get('category')}")
                    print(f"   Тональность: {data.get('sentiment')}")
                    self.results["complaint_creation"] = True
                    self.results["complaint_id"] = data.get('id')
                    return True
                else:
                    print(f"❌ Ошибка создания жалобы: {response.status_code}")
                    print(f"   Ответ: {response.text}")
                    self.results["complaint_creation"] = False
                    return False
        except Exception as e:
            print(f"❌ Ошибка создания жалобы: {e}")
            self.results["complaint_creation"] = False
            return False
    
    async def test_telegram_notification(self):
        """Тестирование Telegram уведомлений"""
        print("🤖 Тестирование Telegram уведомлений...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/telegram/test/")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        print("✅ Telegram уведомление отправлено")
                        self.results["telegram"] = True
                        return True
                    else:
                        print(f"❌ Telegram ошибка: {data.get('message')}")
                        self.results["telegram"] = False
                        return False
                else:
                    print(f"❌ Ошибка Telegram API: {response.status_code}")
                    self.results["telegram"] = False
                    return False
        except Exception as e:
            print(f"❌ Ошибка Telegram: {e}")
            self.results["telegram"] = False
            return False
    
    async def test_complaints_list(self):
        """Тестирование получения списка жалоб"""
        print("📋 Тестирование получения списка жалоб...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/complaints/")
                
                if response.status_code == 200:
                    complaints = response.json()
                    print(f"✅ Получено жалоб: {len(complaints)}")
                    self.results["complaints_list"] = True
                    return True
                else:
                    print(f"❌ Ошибка получения жалоб: {response.status_code}")
                    self.results["complaints_list"] = False
                    return False
        except Exception as e:
            print(f"❌ Ошибка получения жалоб: {e}")
            self.results["complaints_list"] = False
            return False
    
    async def test_recent_complaints(self):
        """Тестирование получения недавних жалоб"""
        print("🕐 Тестирование получения недавних жалоб...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/complaints/recent/?hours=1")
                
                if response.status_code == 200:
                    complaints = response.json()
                    print(f"✅ Недавних жалоб: {len(complaints)}")
                    self.results["recent_complaints"] = True
                    return True
                else:
                    print(f"❌ Ошибка получения недавних жалоб: {response.status_code}")
                    self.results["recent_complaints"] = False
                    return False
        except Exception as e:
            print(f"❌ Ошибка получения недавних жалоб: {e}")
            self.results["recent_complaints"] = False
            return False
    
    async def test_daily_report(self):
        """Тестирование ежедневного отчета"""
        print("📊 Тестирование ежедневного отчета...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/telegram/daily-report/")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        report_data = data.get("data", {})
                        print(f"✅ Отчет отправлен")
                        print(f"   Всего жалоб: {report_data.get('total_complaints', 0)}")
                        print(f"   Открытых жалоб: {report_data.get('open_complaints', 0)}")
                        self.results["daily_report"] = True
                        return True
                    else:
                        print(f"❌ Ошибка отчета: {data.get('message')}")
                        self.results["daily_report"] = False
                        return False
                else:
                    print(f"❌ Ошибка отчета API: {response.status_code}")
                    self.results["daily_report"] = False
                    return False
        except Exception as e:
            print(f"❌ Ошибка отчета: {e}")
            self.results["daily_report"] = False
            return False
    
    async def test_google_sheets_setup(self):
        """Тестирование настройки Google Sheets"""
        print("📊 Тестирование настройки Google Sheets...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/sheets/setup/")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        print("✅ Google Sheets настроены")
                        self.results["google_sheets_setup"] = True
                        return True
                    else:
                        print(f"❌ Ошибка настройки: {data.get('message')}")
                        self.results["google_sheets_setup"] = False
                        return False
                else:
                    print(f"❌ Ошибка настройки API: {response.status_code}")
                    self.results["google_sheets_setup"] = False
                    return False
        except Exception as e:
            print(f"❌ Ошибка настройки: {e}")
            self.results["google_sheets_setup"] = False
            return False
    
    async def test_google_sheets_summary(self):
        """Тестирование получения сводки Google Sheets"""
        print("📈 Тестирование сводки Google Sheets...")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/sheets/summary/")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        summary = data.get("data", {})
                        print(f"✅ Сводка получена: {summary.get('total_complaints', 0)} жалоб")
                        self.results["google_sheets_summary"] = True
                        return True
                    else:
                        print(f"❌ Ошибка сводки: {data.get('message')}")
                        self.results["google_sheets_summary"] = False
                        return False
                else:
                    print(f"❌ Ошибка сводки API: {response.status_code}")
                    self.results["google_sheets_summary"] = False
                    return False
        except Exception as e:
            print(f"❌ Ошибка сводки: {e}")
            self.results["google_sheets_summary"] = False
            return False
    
    def print_summary(self):
        """Вывод итогового отчета"""
        print("\n" + "="*50)
        print("📊 ИТОГОВЫЙ ОТЧЕТ")
        print("="*50)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result is True)
        
        print(f"Всего тестов: {total_tests}")
        print(f"Пройдено: {passed_tests}")
        print(f"Провалено: {total_tests - passed_tests}")
        print(f"Успешность: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\n📋 Детали:")
        for test_name, result in self.results.items():
            status = "✅" if result else "❌"
            print(f"   {status} {test_name}")
        
        if passed_tests == total_tests:
            print("\n🎉 Все тесты пройдены! Система работает корректно.")
        else:
            print("\n⚠️  Некоторые тесты провалены. Проверьте настройки.")
    
    async def run_all_tests(self):
        """Запуск всех тестов"""
        print("🚀 Запуск тестирования интеграции")
        print("="*50)
        
        # Запускаем тесты
        await self.test_health_check()
        await self.test_complaint_creation()
        await self.test_telegram_notification()
        await self.test_complaints_list()
        await self.test_recent_complaints()
        await self.test_daily_report()
        await self.test_google_sheets_setup()
        await self.test_google_sheets_summary()
        
        # Выводим итоги
        self.print_summary()

async def main():
    """Основная функция"""
    tester = IntegrationTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 