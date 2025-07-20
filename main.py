import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

from app.routes import complaints_router, telegram_router, sheets_router

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

# Подключение маршрутов
app.include_router(complaints_router)
app.include_router(telegram_router)
app.include_router(sheets_router)

@app.get("/health/")
async def health_check():
    """Проверка здоровья API"""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 