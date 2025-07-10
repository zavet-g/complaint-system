import httpx
import os
from openai import OpenAI
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
import asyncio
import functools

load_dotenv()

class SentimentService:
    def __init__(self):
        self.api_key = os.getenv("SENTIMENT_API_KEY")
        self.base_url = "https://api.apilayer.com/sentiment/analysis"
    
    async def analyze_sentiment(self, text: str) -> str:
        """Анализ тональности текста через APILayer или простые правила"""
        if not self.api_key:
            return self._simple_sentiment_analysis(text)
        
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
                    # Проверяем, не вернул ли API ошибку
                    if "result" in data and "Unable to evaluate expression" in data["result"]:
                        print(f"Sentiment API cannot process text: {text[:50]}...")
                        return self._simple_sentiment_analysis(text)
                    
                    sentiment = data.get("sentiment", "unknown")
                    return sentiment.lower()
                else:
                    print(f"Sentiment API error: {response.status_code}")
                    return self._simple_sentiment_analysis(text)
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return self._simple_sentiment_analysis(text)
    
    def _simple_sentiment_analysis(self, text: str) -> str:
        """Простой анализ тональности на основе ключевых слов"""
        print(f"DEBUG: [SENTIMENT] Start analysis for: {text}")
        text_lower = text.lower()
        
        # Негативные слова
        negative_words = [
            'плохо', 'ужасно', 'отвратительно', 'не работает', 'ошибка',
            'проблема', 'неудобно', 'медленно', 'зависает', 'вылетает',
            'не загружается', 'баг', 'глюк', 'сломано', 'неправильно',
            'неудовлетворительно', 'разочарован', 'злой', 'раздражен',
            'грубят', 'хамство', 'некомпетентно', 'обман', 'разочарование',
            'негатив', 'ненавижу', 'ненависть', 'кошмар', 'катастрофа',
            'отстой', 'бесполезно', 'бесполезный', 'бесполезная', 'бесполезное',
            'бесполезные', 'бесполезен', 'бесполезна', 'бесполезно', 'бесполезны'
        ]
        
        # Позитивные слова
        positive_words = ['хорошо', 'отлично', 'прекрасно', 'удобно', 'быстро', 
                         'работает', 'нравится', 'доволен', 'спасибо', 'благодарен',
                         'рекомендую', 'супер', 'класс', 'замечательно']
        
        # Нейтральные слова
        neutral_words = ['информация', 'вопрос', 'уточнение', 'просьба', 'запрос',
                        'сообщение', 'уведомление', 'статус', 'проверить']
        
        # Подсчитываем слова
        negative_count = sum(1 for word in negative_words if word in text_lower)
        positive_count = sum(1 for word in positive_words if word in text_lower)
        neutral_count = sum(1 for word in neutral_words if word in text_lower)
        
        print(f"DEBUG: [SENTIMENT] Negative: {negative_count}, Positive: {positive_count}, Neutral: {neutral_count}")
        
        # Определяем тональность
        if negative_count > positive_count and negative_count > 0:
            result = "negative"
        elif positive_count > negative_count and positive_count > 0:
            result = "positive"
        elif neutral_count > 0 or (negative_count == 0 and positive_count == 0):
            result = "neutral"
        else:
            result = "neutral"
        print(f"DEBUG: [SENTIMENT] Result: {result}")
        return result

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
        if not ip or ip == "unknown":
            return {}
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/{ip}",
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"IP API error: {response.status_code} for IP {ip}")
                    return {}
        except Exception as e:
            print(f"Error getting location for IP {ip}: {e}")
            return {}

class AICategoryService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    async def categorize_complaint(self, text: str) -> str:
        """Определение категории жалобы с помощью OpenAI или простых правил"""
        print(f"DEBUG: API key exists: {bool(self.api_key)}, Client exists: {bool(self.client)}")
        if not self.api_key or not self.client:
            print(f"DEBUG: Using simple categorization for: {text}")
            return self._simple_categorization(text)
        
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
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                print(f"OpenAI API quota exceeded, using fallback categorization for: {text[:50]}...")
            else:
                print(f"Error categorizing complaint: {e}")
            # Fallback на простую категоризацию
            return self._simple_categorization(text)
    
    def _simple_categorization(self, text: str) -> str:
        """Простая категоризация на основе ключевых слов"""
        text_lower = text.lower()
        
        # Технические проблемы
        tech_keywords = ['сайт', 'приложение', 'ошибка', 'не работает', 'зависает', 'вылетает', 
                        'не загружается', 'медленно', 'баг', 'глюк', 'техническая', 'программа']
        if any(keyword in text_lower for keyword in tech_keywords):
            return "техническая"
        
        # Проблемы с оплатой
        payment_keywords = ['деньги', 'оплата', 'платеж', 'счет', 'списали', 'дважды', 
                           'возврат', 'штраф', 'комиссия', 'цена', 'стоимость']
        if any(keyword in text_lower for keyword in payment_keywords):
            return "оплата"
        
        # По умолчанию
        return "другое"

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

class GoogleSheetsService:
    def __init__(self):
        self.credentials_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "google-credentials.json")
        self.spreadsheet_id = str(os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", ""))
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
        if not self.worksheet:
            print("Google Sheets not configured or worksheet not available")
            return False
        try:
            loop = asyncio.get_running_loop()
            headers = await loop.run_in_executor(None, self.worksheet.row_values, 1)
            if not headers or len(headers) < 8:
                headers_list = [
                    "ID", "Текст", "Категория", "Тональность", 
                    "Статус", "IP адрес", "Дата создания", "Спам"
                ]
                update_partial = functools.partial(self.worksheet.update, 'A1:H1', [headers_list])  # type: ignore
                await loop.run_in_executor(None, update_partial)
                print("Google Sheets headers created")
            return True
        except Exception as e:
            print(f"Error creating headers: {e}")
            return False
    
    async def add_complaint_to_sheet(self, complaint_data: Dict[str, Any]) -> bool:
        """Добавление жалобы в Google Sheets"""
        if not self.worksheet:
            print("Google Sheets not configured or worksheet not available")
            return False
        try:
            await self.create_headers_if_needed()
            row_data = [
                complaint_data.get('id', ''),
                complaint_data.get('text', '')[:1000],
                complaint_data.get('category', ''),
                complaint_data.get('sentiment', ''),
                complaint_data.get('status', ''),
                complaint_data.get('ip_address', ''),
                complaint_data.get('created_at', ''),
                'Да' if complaint_data.get('is_spam', False) else 'Нет'
            ]
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.worksheet.append_row, row_data)
            print(f"Successfully added complaint {complaint_data.get('id')} to Google Sheets")
            return True
        except Exception as e:
            print(f"Error adding complaint {complaint_data.get('id')} to Google Sheets: {e}")
            return False
    
    async def get_complaints_summary(self) -> Optional[Dict[str, Any]]:
        """Получение сводки жалоб из Google Sheets"""
        if not self.worksheet:
            print("Google Sheets not configured or worksheet not available")
            return None
        try:
            loop = asyncio.get_running_loop()
            all_values = await loop.run_in_executor(None, self.worksheet.get_all_values)
            if len(all_values) <= 1:
                return {
                    "total_complaints": 0,
                    "categories": {},
                    "sentiments": {},
                    "statuses": {}
                }
            data_rows = all_values[1:]
            summary = {
                "total_complaints": len(data_rows),
                "categories": {},
                "sentiments": {},
                "statuses": {}
            }
            for row in data_rows:
                if len(row) >= 5:
                    category = row[2] if len(row) > 2 else "Неизвестно"
                    sentiment = row[3] if len(row) > 3 else "Неизвестно"
                    status = row[4] if len(row) > 4 else "Неизвестно"
                    summary["categories"][category] = summary["categories"].get(category, 0) + 1
                    summary["sentiments"][sentiment] = summary["sentiments"].get(sentiment, 0) + 1
                    summary["statuses"][status] = summary["statuses"].get(status, 0) + 1
            print(f"Successfully retrieved summary from Google Sheets: {summary['total_complaints']} complaints")
            return summary
        except Exception as e:
            print(f"Error getting summary from Google Sheets: {e}")
            return None 