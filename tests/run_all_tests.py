#!/usr/bin/env python3
"""
Главный файл для запуска всех тестов системы обработки жалоб
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_test_file(test_file: str, description: str) -> bool:
    """Запуск отдельного тестового файла"""
    print(f"\n🧪 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Успешно")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Ошибка")
            if result.stderr:
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Таймаут")
        return False
    except Exception as e:
        print(f"💥 Исключение: {e}")
        return False

def main():
    """Запуск всех тестов"""
    print("🚀 Запуск всех тестов системы обработки жалоб")
    print("=" * 60)
    
    # Определяем тесты
    tests = [
        ("tests/unit/test_telegram.py", "Тест Telegram интеграции"),
        ("tests/unit/test_google_sheets.py", "Тест Google Sheets интеграции"),
        ("tests/unit/test_sheets.py", "Тест Google Sheets API"),
        ("tests/api/test_api.py", "Тест API endpoints"),
        ("tests/integration/test_integration.py", "Интеграционные тесты"),
    ]
    
    # Проверяем, что сервер запущен
    print("\n🔍 Проверка доступности сервера...")
    try:
        import requests
        response = requests.get("http://localhost:8000/health/", timeout=5)
        if response.status_code == 200:
            print("✅ Сервер доступен")
        else:
            print("⚠️ Сервер отвечает, но неожиданный статус")
    except Exception as e:
        print(f"❌ Сервер недоступен: {e}")
        print("💡 Запустите сервер: python main.py")
        return
    
    # Запускаем тесты
    passed = 0
    total = len(tests)
    
    for test_file, description in tests:
        if os.path.exists(test_file):
            if run_test_file(test_file, description):
                passed += 1
        else:
            print(f"⚠️ Файл не найден: {test_file}")
    
    # Итоговый отчет
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    print(f"Всего тестов: {total}")
    print(f"Пройдено: {passed}")
    print(f"Провалено: {total - passed}")
    print(f"Успешность: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 Все тесты прошли успешно!")
    else:
        print(f"\n⚠️ {total - passed} тестов провалились")

if __name__ == "__main__":
    main() 