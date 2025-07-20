from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ..models.database import get_db, Complaint
from ..services import GoogleSheetsService

router = APIRouter(prefix="/sheets", tags=["sheets"])

# Инициализация сервиса
sheets_service = GoogleSheetsService()

@router.post("/setup/")
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

@router.get("/summary/")
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

@router.post("/export/")
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