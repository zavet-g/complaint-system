import httpx
import os
from typing import Dict, Any

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