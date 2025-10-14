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
                if response.status == 201:  # 201 Created (как мы настроили в View)
                    logger.info(f"Триал для {tg_id} успешно активирован.")
                    return await response.json()

                # Код 400 BAD REQUEST, если триал уже использован или есть подписка
                elif response.status == 400:
                    error_detail = await response.json()
                    logger.warning(f"Триал недоступен для {tg_id}. Детали: {error_detail}")
                    return {"error": error_detail.get("error", "Триал недоступен.")}

                else:
                    error_detail = await response.json()
                    logger.error(
                        f"Ошибка API при активации триала для {tg_id}. Статус: {response.status}. Детали: {error_detail}")
                    return None
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Ошибка подключения к API {url}: {e}")
            return None

    # TODO: Добавить метод purchase_tariff
    # async def purchase_tariff(self, tg_id: int, tariff_slug: str, duration_months: int) -> Optional[Dict[str, Any]]:
    #     url = f"{self.base_url}purchase_tariff/"
    #     payload = {"user_id": tg_id, "tariff_slug": tariff_slug, "duration_months": duration_months}
    #     ...
    #     pass