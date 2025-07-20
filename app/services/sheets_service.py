import os
import asyncio
import functools
from typing import Dict, Any, Optional
import gspread
from google.oauth2.service_account import Credentials

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