import httpx
import os
from typing import Dict, Any

class TelegramService:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id_str = os.getenv("TELEGRAM_CHAT_ID")
        # Преобразуем chat_id в число
        try:
            self.chat_id = int(chat_id_str) if chat_id_str else None
        except (ValueError, TypeError):
            self.chat_id = None
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    async def send_notification(self, message: str, parse_mode: str = "HTML") -> bool:
        """Отправка уведомления в Telegram"""
        if not self.bot_token or not self.chat_id:
            print("Telegram bot not configured")
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": parse_mode
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("ok", False)
                else:
                    print(f"Telegram API error: {response.status_code}")
                    return False
        except Exception as e:
            print(f"Error sending Telegram notification: {e}")
            return False
    
    async def send_complaint_notification(self, complaint_data: Dict[str, Any]) -> bool:
        """Отправка уведомления о новой жалобе"""
        if not self.bot_token or not self.chat_id:
            print("Telegram bot not configured")
            return False
        
        try:
            # Формируем красивое сообщение
            message = f"""
🚨 <b>Новая жалоба #{complaint_data.get('id', 'N/A')}</b>

📝 <b>Текст:</b> {complaint_data.get('text', 'N/A')}

🏷️ <b>Категория:</b> {complaint_data.get('category', 'N/A')}
😊 <b>Тональность:</b> {complaint_data.get('sentiment', 'N/A')}
📍 <b>IP:</b> {complaint_data.get('ip_address', 'N/A')}
🕐 <b>Время:</b> {complaint_data.get('created_at', 'N/A')}

{'⚠️ <b>Спам:</b> Да' if complaint_data.get('is_spam', False) else ''}
            """.strip()
            
            success = await self.send_notification(message)
            if success:
                print(f"Successfully sent Telegram notification for complaint {complaint_data.get('id')}")
            else:
                print(f"Failed to send Telegram notification for complaint {complaint_data.get('id')}")
            return success
        except Exception as e:
            print(f"Error sending Telegram notification for complaint {complaint_data.get('id')}: {e}")
            return False
    
    async def send_daily_report(self, complaints_count: int, open_complaints: int) -> bool:
        """Отправка ежедневного отчета"""
        if not self.bot_token or not self.chat_id:
            print("Telegram bot not configured for daily report")
            return False
        
        try:
            message = f"""
📊 <b>Ежедневный отчет</b>

📈 <b>Всего жалоб за день:</b> {complaints_count}
🔴 <b>Открытых жалоб:</b> {open_complaints}
✅ <b>Обработано:</b> {complaints_count - open_complaints}

🕐 Отчет сформирован автоматически
            """.strip()
            
            success = await self.send_notification(message)
            if success:
                print(f"Successfully sent daily report: {complaints_count} total, {open_complaints} open")
            else:
                print(f"Failed to send daily report")
            return success
        except Exception as e:
            print(f"Error sending daily report: {e}")
            return False 