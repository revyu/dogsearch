import httpx
from typing import Dict, Any, List, Optional

from app.config.settings import settings

class VKService:
    """
    Сервис для взаимодействия с API ВКонтакте
    """
    API_VERSION = "5.131"
    API_URL = "https://api.vk.com/method/"
    
    def __init__(self):
        self.service_key = settings.VK_SERVICE_KEY
        
    async def _make_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполнить запрос к API ВКонтакте
        """
        params.update({
            "v": self.API_VERSION,
            "access_token": self.service_key
        })
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.API_URL}{method}", params=params)
            return response.json()
    
    async def get_user_info(self, user_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Получить информацию о пользователях
        """
        params = {
            "user_ids": ",".join(map(str, user_ids)),
            "fields": "photo_200"
        }
        
        response = await self._make_request("users.get", params)
        return response.get("response", [])
        
    async def get_group_posts(self, group_id: int, count: int = 100) -> List[Dict[str, Any]]:
        """
        Получить посты из группы
        """
        params = {
            "owner_id": -group_id,  # Минус для групп
            "count": count
        }
        
        response = await self._make_request("wall.get", params)
        return response.get("response", {}).get("items", [])
