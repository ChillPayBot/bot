import aiohttp
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class SubscriptionAPIService:
    """Сервис для обращения к Django REST API по управлению подписками (/subscriptions/)."""

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        self.base_url = base_url.rstrip('/') + '/subscriptions/'
        self.session = session

    async def activate_trial(self, tg_id: int) -> Optional[Dict[str, Any]]:
        """
        Активирует пробный период для пользователя.
        POST /subscriptions/activate_trial/
        """
        url = f"{self.base_url}activate_trial/"
        payload = {"user_id": tg_id}

        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 201:
                    logger.info(f"Триал для {tg_id} успешно активирован.")
                    return await response.json()

                elif response.status == 400:
                    error_detail = await response.json()
                    return {"error": error_detail.get("error", "Триал недоступен.")}

                else:
                    return None
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Ошибка подключения к API {url}: {e}")
            return None