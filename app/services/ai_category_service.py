import os
from openai import OpenAI

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