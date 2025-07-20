from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from ..models.database import get_db, Complaint
from ..services import TelegramService

router = APIRouter(prefix="/telegram", tags=["telegram"])

# Инициализация сервиса
telegram_service = TelegramService()

@router.post("/test/")
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

@router.post("/daily-report/")
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