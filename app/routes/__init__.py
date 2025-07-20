"""
API маршруты для системы обработки жалоб
"""

from .complaints import router as complaints_router
from .telegram import router as telegram_router
from .sheets import router as sheets_router

__all__ = [
    'complaints_router',
    'telegram_router',
    'sheets_router'
] 