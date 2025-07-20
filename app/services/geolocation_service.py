import httpx
from typing import Dict, Any

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