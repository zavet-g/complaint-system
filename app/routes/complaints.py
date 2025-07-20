from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import asyncio
from typing import Optional

from ..models.database import get_db, Complaint
from ..models.schemas import ComplaintCreate, ComplaintResponse, ComplaintUpdate
from ..services import SentimentService, AICategoryService, SpamService, GeolocationService, TelegramService, GoogleSheetsService

router = APIRouter(prefix="/complaints", tags=["complaints"])

# Инициализация сервисов
sentiment_service = SentimentService()
ai_category_service = AICategoryService()
spam_service = SpamService()
geolocation_service = GeolocationService()
telegram_service = TelegramService()
sheets_service = GoogleSheetsService()

@router.post("/", response_model=ComplaintResponse)
async def create_complaint(
    complaint: ComplaintCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Создание новой жалобы с анализом тональности и категоризацией"""
    try:
        # Проверка на спам (опционально)
        spam_result = await spam_service.check_spam(complaint.text)
        
        # Анализ тональности
        print(f"DEBUG: [MAIN] About to analyze sentiment for: {complaint.text[:50]}...")
        sentiment = await sentiment_service.analyze_sentiment(complaint.text)
        print(f"DEBUG: [MAIN] Sentiment result: {sentiment}")
        
        # Определение категории с помощью ИИ
        category = await ai_category_service.categorize_complaint(complaint.text)
        
        # Получение IP клиента для геолокации (опционально)
        client_ip = request.client.host if request.client else "unknown"
        location = await geolocation_service.get_location(client_ip)
        
        # Создание записи в базе данных
        db_complaint = Complaint(
            text=complaint.text,
            sentiment=sentiment,
            category=category
        )
        
        db.add(db_complaint)
        db.commit()
        db.refresh(db_complaint)
        
        # Отправка уведомления в Telegram (асинхронно)
        try:
            complaint_data = {
                "id": db_complaint.id,
                "text": db_complaint.text,
                "category": db_complaint.category,
                "sentiment": db_complaint.sentiment,
                "status": db_complaint.status,
                "ip_address": client_ip,
                "created_at": db_complaint.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "is_spam": spam_result.get("is_spam", False)
            }
            
            # Отправляем уведомление в фоне (не блокируем ответ)
            asyncio.create_task(telegram_service.send_complaint_notification(complaint_data))
            
            # Добавляем в Google Sheets (асинхронно)
            asyncio.create_task(sheets_service.add_complaint_to_sheet(complaint_data))
        except Exception as e:
            print(f"Error sending notifications: {e}")
        
        return ComplaintResponse(
            id=db_complaint.id,
            status=db_complaint.status,
            sentiment=db_complaint.sentiment,
            category=db_complaint.category
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/", response_model=list[ComplaintResponse])
async def get_complaints(
    status: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получение списка жалоб с фильтрацией"""
    try:
        query = db.query(Complaint)
        
        if status:
            query = query.filter(Complaint.status == status)
        if category:
            query = query.filter(Complaint.category == category)
            
        complaints = query.limit(limit).all()
        
        return [
            ComplaintResponse(
                id=c.id,
                status=c.status,
                sentiment=c.sentiment,
                category=c.category
            ) for c in complaints
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/recent/", response_model=list[ComplaintResponse])
async def get_recent_complaints(
    hours: int = 1,
    status: str = "open",
    db: Session = Depends(get_db)
):
    """Получение жалоб за последние N часов (для n8n)"""
    try:
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        complaints = db.query(Complaint).filter(
            Complaint.status == status,
            Complaint.timestamp >= time_threshold
        ).all()
        
        return [
            ComplaintResponse(
                id=c.id,
                status=c.status,
                sentiment=c.sentiment,
                category=c.category
            ) for c in complaints
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/{complaint_id}/", response_model=ComplaintResponse)
async def update_complaint(
    complaint_id: int,
    complaint_update: ComplaintUpdate,
    db: Session = Depends(get_db)
):
    """Обновление статуса жалобы (для n8n)"""
    try:
        db_complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
        
        if not db_complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")
        
        # Обновление полей
        if complaint_update.status is not None:
            db_complaint.status = complaint_update.status
        if complaint_update.sentiment is not None:
            db_complaint.sentiment = complaint_update.sentiment
        if complaint_update.category is not None:
            db_complaint.category = complaint_update.category
        
        db.commit()
        db.refresh(db_complaint)
        
        return ComplaintResponse(
            id=db_complaint.id,
            status=db_complaint.status,
            sentiment=db_complaint.sentiment,
            category=db_complaint.category
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/{complaint_id}/", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    """Получение конкретной жалобы по ID"""
    try:
        db_complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
        
        if not db_complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")
        
        return ComplaintResponse(
            id=db_complaint.id,
            status=db_complaint.status,
            sentiment=db_complaint.sentiment,
            category=db_complaint.category
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 