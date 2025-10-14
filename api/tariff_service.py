import aiohttp
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class TariffAPIService:
    """Сервис для обращения к Django REST API по управлению тарифами (/tariffs/)."""

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        self.base_url = base_url.rstrip('/') + '/tariffs/'
        self.session = session

    async def get_active_tariffs(self) -> Optional[List[Dict[str, Any]]]:
        """
        Получает список активных тарифов.
        GET /tariffs/
        """
        url = self.base_url
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    logger.warning("Тарифы не найдены (404), возможно, они не созданы.")
                    return []
                else:
                    error_detail = await response.json()
                    logger.error(
                        f"Ошибка API при GET тарифов. Статус: {response.status}. Детали: {error_detail}"
                    )
                    return None
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Ошибка подключения к API {url}: {e}")
            return None
