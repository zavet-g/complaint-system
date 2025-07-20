from fastapi import Request
from datetime import datetime, timezone

def get_client_ip(request: Request) -> str:
    """Получение IP адреса клиента"""
    if request.client:
        return request.client.host
    return "unknown"

def format_datetime(dt: datetime) -> str:
    """Форматирование даты и времени"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S") 