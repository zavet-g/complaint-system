"""
Модели данных для системы обработки жалоб
"""

from .database import Base, Complaint
from .schemas import ComplaintCreate, ComplaintUpdate, ComplaintResponse

__all__ = [
    'Base',
    'Complaint', 
    'ComplaintCreate',
    'ComplaintUpdate',
    'ComplaintResponse'
] 