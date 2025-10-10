import aiohttp
import logging
from config.settings import Settings
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


SettingsData = Dict[str, Any]


class SettingsService:

    DEFAULT_SETTINGS: SettingsData = {
        "is_trial_enabled": False,
        "default_trial_days": 7,
        "min_top_up_amount": 100,
        "bot_username": "YourBotUsernamePlaceholder"
    }

    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip('/')

        self.headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        }
        self.session = aiohttp.ClientSession(headers=self.headers)
        self.settings_endpoint = f"{self.base_url}/settings/"

    async def close(self):
        """Закрывает сессию aiohttp."""
        await self.session.close()

    async def get_global_settings(self) -> SettingsData:
        """
        Отправляет GET-запрос в Django и возвращает глобальные настройки.
        Возвращает дефолтные значения в случае ошибки.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.settings_endpoint, timeout=5) as response:

                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Настройки успешно загружены из Django API.")
                        return data
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"Ошибка Django API при получении настроек (Status: {response.status}). "
                            f"URL: {self.settings_endpoint}."
                        )
                        return self.DEFAULT_SETTINGS

            except aiohttp.ClientConnectorError:
                logger.error(f"Ошибка соединения с Django API по URL: {self.settings_endpoint}")
                return self.DEFAULT_SETTINGS

            except Exception as e:
                logger.error(f"Неожиданная ошибка при запросе настроек: {e}", exc_info=True)
                return self.DEFAULT_SETTINGS
