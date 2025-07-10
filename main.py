import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import asyncio
from typing import Optional

from database import get_db, Complaint
from models import ComplaintCreate, ComplaintResponse, ComplaintUpdate
from services import SentimentService, AICategoryService, SpamService, GeolocationService, TelegramService, GoogleSheetsService

app = FastAPI(
    title="Complaint Processing System",
    description="API для обработки жалоб клиентов с интеграцией внешних сервисов",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация сервисов
sentiment_service = SentimentService()
ai_category_service = AICategoryService()
spam_service = SpamService()
geolocation_service = GeolocationService()
telegram_service = TelegramService()
sheets_service = GoogleSheetsService()

@app.post("/complaints/", response_model=ComplaintResponse)
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

@app.get("/complaints/", response_model=list[ComplaintResponse])
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

@app.get("/complaints/recent/", response_model=list[ComplaintResponse])
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

@app.put("/complaints/{complaint_id}/", response_model=ComplaintResponse)
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

@app.get("/complaints/{complaint_id}/", response_model=ComplaintResponse)
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

@app.get("/health/")
async def health_check():
    """Проверка здоровья API"""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

@app.post("/telegram/test/")
async def test_telegram():
    """Тестирование Telegram уведомлений"""
    try:
        success = await telegram_service.send_notification(
            "🧪 <b>Тестовое уведомление</b>\n\n✅ Telegram интеграция работает!"
        )
        
        if success:
            return {"status": "success", "message": "Telegram notification sent"}
        else:
            return {"status": "error", "message": "Failed to send Telegram notification"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Telegram error: {str(e)}")

@app.post("/telegram/daily-report/")
async def send_daily_report(db: Session = Depends(get_db)):
    """Отправка ежедневного отчета в Telegram"""
    try:
        # Подсчет жалоб за последние 24 часа
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        total_complaints = db.query(Complaint).filter(
            Complaint.timestamp >= yesterday
        ).count()
        
        open_complaints = db.query(Complaint).filter(
            Complaint.status == "open",
            Complaint.timestamp >= yesterday
        ).count()
        
        success = await telegram_service.send_daily_report(total_complaints, open_complaints)
        
        if success:
            return {
                "status": "success", 
                "message": "Daily report sent",
                "data": {
                    "total_complaints": total_complaints,
                    "open_complaints": open_complaints
                }
            }
        else:
            return {"status": "error", "message": "Failed to send daily report"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report error: {str(e)}")

@app.post("/sheets/setup/")
async def setup_google_sheets():
    """Настройка Google Sheets (создание заголовков)"""
    try:
        success = await sheets_service.create_headers_if_needed()
        
        if success:
            return {"status": "success", "message": "Google Sheets headers created"}
        else:
            return {"status": "error", "message": "Failed to setup Google Sheets"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sheets setup error: {str(e)}")

@app.get("/sheets/summary/")
async def get_sheets_summary():
    """Получение сводки из Google Sheets"""
    try:
        summary = await sheets_service.get_complaints_summary()
        
        if summary:
            return {
                "status": "success",
                "data": summary
            }
        else:
            return {"status": "error", "message": "Failed to get summary from Google Sheets"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sheets summary error: {str(e)}")

@app.post("/sheets/export/")
async def export_complaints_to_sheets(db: Session = Depends(get_db)):
    """Экспорт всех жалоб в Google Sheets"""
    try:
        # Получаем все жалобы
        complaints = db.query(Complaint).all()
        
        exported_count = 0
        for complaint in complaints:
            complaint_data = {
                "id": complaint.id,
                "text": complaint.text,
                "category": complaint.category,
                "sentiment": complaint.sentiment,
                "status": complaint.status,
                "created_at": complaint.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": "N/A",
                "is_spam": False
            }
            
            if await sheets_service.add_complaint_to_sheet(complaint_data):
                exported_count += 1
        
        return {
            "status": "success",
            "message": f"Exported {exported_count} complaints to Google Sheets",
            "data": {
                "total_complaints": len(complaints),
                "exported_count": exported_count
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 