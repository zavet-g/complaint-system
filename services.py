import httpx
import os
import openai
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class SentimentService:
    def __init__(self):
        self.api_key = os.getenv("SENTIMENT_API_KEY")
        self.base_url = "https://api.apilayer.com/sentiment/analysis"
    
    async def analyze_sentiment(self, text: str) -> str:
        """Анализ тональности текста через APILayer"""
        if not self.api_key:
            return "unknown"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers={"apikey": self.api_key},
                    json={"text": text},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    sentiment = data.get("sentiment", "unknown")
                    return sentiment.lower()
                else:
                    return "unknown"
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return "unknown"

class SpamService:
    def __init__(self):
        self.api_key = os.getenv("SPAM_API_KEY")
        self.base_url = "https://api.api-ninjas.com/v1/spamcheck"
    
    async def check_spam(self, text: str) -> Dict[str, Any]:
        """Проверка на спам через API Ninjas"""
        if not self.api_key:
            return {"is_spam": False, "score": 0}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.base_url,
                    headers={"X-Api-Key": self.api_key},
                    params={"text": text},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"is_spam": False, "score": 0}
        except Exception as e:
            print(f"Error checking spam: {e}")
            return {"is_spam": False, "score": 0}

class GeolocationService:
    def __init__(self):
        self.base_url = "http://ip-api.com/json"
    
    async def get_location(self, ip: str) -> Dict[str, Any]:
        """Получение геолокации по IP через IP API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/{ip}",
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {}
        except Exception as e:
            print(f"Error getting location: {e}")
            return {}

class AICategoryService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
    
    async def categorize_complaint(self, text: str) -> str:
        """Определение категории жалобы с помощью OpenAI"""
        if not self.api_key:
            return "другое"
        
        try:
            prompt = f'Определи категорию жалобы: "{text}". Варианты: техническая, оплата, другое. Ответ только одним словом.'
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты помощник для категоризации жалоб клиентов."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            category = response.choices[0].message.content.strip().lower()
            
            # Валидация категории
            valid_categories = ["техническая", "оплата", "другое"]
            if category in valid_categories:
                return category
            else:
                return "другое"
                
        except Exception as e:
            print(f"Error categorizing complaint: {e}")
            return "другое"

class TelegramService:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
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
            return False
        
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
        
        return await self.send_notification(message)
    
    async def send_daily_report(self, complaints_count: int, open_complaints: int) -> bool:
        """Отправка ежедневного отчета"""
        message = f"""
📊 <b>Ежедневный отчет</b>

📈 <b>Всего жалоб за день:</b> {complaints_count}
🔴 <b>Открытых жалоб:</b> {open_complaints}
✅ <b>Обработано:</b> {complaints_count - open_complaints}

🕐 Отчет сформирован автоматически
        """.strip()
        
        return await self.send_notification(message) 