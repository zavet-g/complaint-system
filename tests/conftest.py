"""
Конфигурация для тестов
"""
import pytest
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def test_data():
    """Тестовые данные для жалоб"""
    return {
        "technical_complaint": {
            "text": "Сайт не загружается, постоянно выдает ошибку 500",
            "expected_category": "техническая",
            "expected_sentiment": "negative"
        },
        "payment_complaint": {
            "text": "Списали деньги дважды за одну услугу, нужен возврат",
            "expected_category": "оплата", 
            "expected_sentiment": "negative"
        },
        "positive_feedback": {
            "text": "Отличный сервис! Все работает быстро и удобно. Спасибо!",
            "expected_category": "другое",
            "expected_sentiment": "positive"
        },
        "neutral_request": {
            "text": "Нужна информация о статусе заказа",
            "expected_category": "другое",
            "expected_sentiment": "neutral"
        }
    }

@pytest.fixture
def api_base_url():
    """Базовый URL для API тестов"""
    return "http://localhost:8000"

@pytest.fixture
def headers():
    """Заголовки для API запросов"""
    return {"Content-Type": "application/json"} 