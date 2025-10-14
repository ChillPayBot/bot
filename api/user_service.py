import aiohttp
import logging
from typing import Optional, Dict, Any, Union

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, base_url: str, session: aiohttp.ClientSession):
        self.base_url = base_url.rstrip('/')
        self.session = session

    async def get_user_data(self, tg_id: int) -> Optional[Dict[str, Any]]:
        """Получает данные пользователя по его Telegram ID. GET /users/{tg_id}/"""

        url = f"{self.base_url}/users/{tg_id}/"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                elif response.status == 401:
                    logger.error("Ошибка 401: Неправильный или отсутствующий API токен.")
                    return None
                else:
                    error_detail = await response.json()
                    logger.error(
                        f"Ошибка API при GET пользователя {tg_id}. Статус: {response.status}. "
                        f"Детали: {error_detail}"
                    )
                    return None
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Ошибка подключения к API {url}: {e}")
            return None



    async def add_user(self, user_id: int, username: Optional[str] = None,
                       first_name: Optional[str] = None, last_name: Optional[str] = None,
                       language_code: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Создает нового пользователя. POST /users/"""

        url = f"{self.base_url}/users/"
        payload = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "language_code": language_code,
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 201:
                    logger.info(f"Новый пользователь {user_id} успешно создан (201).")
                    return await response.json()
                elif response.status == 400:
                    error_detail = await response.json()
                    # Если получаем ошибку 400, это может быть конфликт (пользователь уже есть)
                    # или ошибка валидации
                    if 'user_id' in error_detail:  # Проверяем, связано ли с конфликтом PK
                        logger.warning(f"Пользователь {user_id} уже существует или ошибка PK (400).")
                        return {"user_id": user_id, "message": "User already exists (via add_user)."}

                    logger.error(f"Ошибка API при add_user {user_id}. Статус: 400. Детали: {error_detail}")
                    return None
                else:
                    logger.error(f"Ошибка API при add_user {user_id}. Статус: {response.status}")
                    return None

        except aiohttp.ClientConnectorError as e:
            logger.error(f"Ошибка подключения к API {url}: {e}")
            return None

    # --- 3. PATCH_USER (PATCH) ---
    async def patch_user(
            self,
            user_id: int,
            payload: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Обновляет только переданные поля существующего пользователя. PATCH /users/{user_id}/"""

        url = f"{self.base_url}/users/{user_id}/"

        clean_payload = {k: v for k, v in payload.items() if v is not None}
        if not clean_payload: return None

        try:
            async with self.session.patch(url, json=clean_payload) as response:
                if response.status == 200:
                    logger.info(f"Пользователь {user_id} успешно обновлен (200).")
                    return await response.json()
                elif response.status == 404:
                    logger.warning(f"Пользователь {user_id} не найден для PATCH.")
                    return None
                else:
                    logger.error(f"Ошибка API при patch_user {user_id}. Статус: {response.status}")
                    return None
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Ошибка подключения к API {url}: {e}")
            return None