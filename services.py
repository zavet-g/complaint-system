import httpx
import os
from openai import OpenAI
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

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
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    async def categorize_complaint(self, text: str) -> str:
        """Определение категории жалобы с помощью OpenAI"""
        if not self.api_key or not self.client:
            return "другое"
        
        try:
            prompt = f'Определи категорию жалобы: "{text}". Варианты: техническая, оплата, другое. Ответ только одним словом.'
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты помощник для категоризации жалоб клиентов."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            category = response.choices[0].message.content.strip().lower() if response.choices[0].message.content else "другое"
            
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

class GoogleSheetsService:
    def __init__(self):
        self.credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "google-credentials.json")
        self.spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        self.sheet_name = os.getenv("GOOGLE_SHEET_NAME", "Жалобы")
        
        # Настройка Google Sheets API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        
        try:
            print(f"DEBUG: Checking file {self.credentials_file}, exists: {os.path.exists(self.credentials_file)}")
            if os.path.exists(self.credentials_file):
                print(f"DEBUG: Loading credentials from {self.credentials_file}")
                credentials = Credentials.from_service_account_file(
                    self.credentials_file, scopes=scope
                )
                print(f"DEBUG: Authorizing with gspread")
                self.client = gspread.authorize(credentials)
                print(f"DEBUG: Opening spreadsheet {self.spreadsheet_id}")
                self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
                print(f"DEBUG: Available worksheets: {[ws.title for ws in self.spreadsheet.worksheets()]}")
                print(f"DEBUG: Getting worksheet '{self.sheet_name}'")
                self.worksheet = self.spreadsheet.worksheet(self.sheet_name)
                print(f"DEBUG: Successfully initialized Google Sheets")
            else:
                print(f"Google credentials file not found: {self.credentials_file}")
                self.client = None
                self.spreadsheet = None
                self.worksheet = None
        except Exception as e:
            print(f"Error initializing Google Sheets: {e}")
            self.client = None
            self.spreadsheet = None
            self.worksheet = None
    
    async def create_headers_if_needed(self) -> bool:
        """Создание заголовков в Google Sheets если их нет"""
        if not self.worksheet:
            return False
        
        try:
            # Проверяем, есть ли уже заголовки
            headers = self.worksheet.row_values(1)
            if not headers or len(headers) < 8:
                # Создаем заголовки
                headers = [
                    "ID", "Текст", "Категория", "Тональность", 
                    "Статус", "IP адрес", "Дата создания", "Спам"
                ]
                self.worksheet.update('A1:H1', [headers])
                print("Google Sheets headers created")
            return True
        except Exception as e:
            print(f"Error creating headers: {e}")
            return False
    
    async def add_complaint_to_sheet(self, complaint_data: Dict[str, Any]) -> bool:
        """Добавление жалобы в Google Sheets"""
        if not self.worksheet:
            return False
        
        try:
            # Создаем заголовки если нужно
            await self.create_headers_if_needed()
            
            # Подготавливаем данные для записи
            row_data = [
                complaint_data.get('id', ''),
                complaint_data.get('text', ''),
                complaint_data.get('category', ''),
                complaint_data.get('sentiment', ''),
                complaint_data.get('status', ''),
                complaint_data.get('ip_address', ''),
                complaint_data.get('created_at', ''),
                'Да' if complaint_data.get('is_spam', False) else 'Нет'
            ]
            
            # Добавляем новую строку
            self.worksheet.append_row(row_data)
            return True
        except Exception as e:
            print(f"Error adding complaint to sheet: {e}")
            return False
    
    async def get_complaints_summary(self) -> Optional[Dict[str, Any]]:
        """Получение сводки жалоб из Google Sheets"""
        if not self.worksheet:
            return None
        
        try:
            # Получаем все данные
            all_values = self.worksheet.get_all_values()
            
            if len(all_values) <= 1:  # Только заголовки
                return {
                    "total_complaints": 0,
                    "categories": {},
                    "sentiments": {},
                    "statuses": {}
                }
            
            # Пропускаем заголовки
            data_rows = all_values[1:]
            
            summary = {
                "total_complaints": len(data_rows),
                "categories": {},
                "sentiments": {},
                "statuses": {}
            }
            
            # Анализируем данные
            for row in data_rows:
                if len(row) >= 5:
                    category = row[2] if len(row) > 2 else "Неизвестно"
                    sentiment = row[3] if len(row) > 3 else "Неизвестно"
                    status = row[4] if len(row) > 4 else "Неизвестно"
                    
                    summary["categories"][category] = summary["categories"].get(category, 0) + 1
                    summary["sentiments"][sentiment] = summary["sentiments"].get(sentiment, 0) + 1
                    summary["statuses"][status] = summary["statuses"].get(status, 0) + 1
            
            return summary
        except Exception as e:
            print(f"Error getting summary: {e}")
            return None 