import httpx
import os
from typing import Dict, Any

class SentimentService:
    def __init__(self):
        self.api_key = os.getenv("SENTIMENT_API_KEY")
        self.base_url = "https://api.apilayer.com/sentiment/analysis"
    
    async def analyze_sentiment(self, text: str) -> str:
        """Анализ тональности текста через APILayer или простые правила"""
        if not self.api_key:
            print(f"DEBUG: [SENTIMENT] No API key, using fallback analysis")
            return self._simple_sentiment_analysis(text)
        
        try:
            print(f"DEBUG: [SENTIMENT] Trying APILayer API for: {text[:50]}...")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers={"apikey": self.api_key},
                    json={"text": text},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"DEBUG: [SENTIMENT] API response: {data}")
                    # Проверяем, не вернул ли API ошибку
                    if "result" in data and "Unable to evaluate expression" in data["result"]:
                        print(f"DEBUG: [SENTIMENT] API cannot process text, using fallback")
                        return self._simple_sentiment_analysis(text)
                    
                    sentiment = data.get("sentiment", "unknown")
                    print(f"DEBUG: [SENTIMENT] API result: {sentiment}")
                    return sentiment.lower()
                else:
                    print(f"DEBUG: [SENTIMENT] API error: {response.status_code}, response: {response.text}")
                    return self._simple_sentiment_analysis(text)
        except Exception as e:
            print(f"DEBUG: [SENTIMENT] Exception during API call: {e}")
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
            'бесполезные', 'бесполезен', 'бесполезна', 'бесполезно', 'бесполезны',
            'не', 'нет', 'нельзя', 'невозможно', 'неправильно', 'неверно',
            'неудобно', 'неприятно', 'негативно', 'плохой', 'плохая', 'плохое',
            'ужасный', 'ужасная', 'ужасное', 'отвратительный', 'отвратительная',
            'сломан', 'сломана', 'сломано', 'неисправен', 'неисправна',
            'недоступен', 'недоступна', 'недоступно', 'недоступны'
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
        if negative_count > 0:
            if negative_count > positive_count:
                result = "negative"
            elif negative_count == positive_count:
                result = "neutral"
            else:
                result = "positive"
        elif positive_count > 0:
            result = "positive"
        else:
            result = "neutral"
        print(f"DEBUG: [SENTIMENT] Result: {result}")
        return result 