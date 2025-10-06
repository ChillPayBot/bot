import aiohttp
import logging
from config import config

class ApiClient:
    def __init__(self):
        self.base_url = config.API_BASE_URL

    async def register_user(self, user_id: int, username: str, first_name: str, last_name: str):
        """
        Отправляет POST-запрос в NestJS API для регистрации пользователя
        """
        url = f"{self.base_url}/users/register"
        payload = {
            "telegram_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        logging.warning(f"API register_user failed: {resp.status}")
                        return None
            except Exception as e:
                logging.error(f"Error during register_user: {e}")
                return None

    async def get_user_subscription(self, user_id: int):
        """
        Получает информацию о подписке пользователя
        """
        url = f"{self.base_url}/subscriptions/{user_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
            except Exception as e:
                logging.error(f"Error during get_user_subscription: {e}")
                return None
