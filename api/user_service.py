# api/user_service.py (Обновленный)

import aiohttp
import logging
from typing import Optional, Dict, Any, Union

logger = logging.getLogger(__name__)


class UserService:
    # ... (init и close остаются без изменений) ...
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = aiohttp.ClientSession()
        logger.info(f"UserService инициализирован с базовым URL: {self.base_url}")

    async def close(self):
        """Закрывает сессию aiohttp."""
        await self.session.close()

    # --- 1. CHECK_USER_EXISTS / GET USER DATA (GET) ---
    async def get_user_data(self, tg_id: int) -> Optional[Dict[str, Any]]:
        """
        Проверяет, существует ли пользователь, и возвращает его данные.
        GET /api/v1/users/{tg_id}/
        """
        url = f"{self.base_url}/users/{tg_id}/"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None  # Пользователь не найден
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

    # --- 2. ADD_USER (POST) ---
    async def add_user(
            self,
            tg_id: int,
            username: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            language_code: Optional[str] = None,
            is_bot: bool = False,
            source_code: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Создает нового пользователя. Ожидает HTTP 201.
        POST /api/v1/users/
        """
        url = f"{self.base_url}/users/"
        payload = {
            "tg_id": tg_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "language_code": language_code,
            "is_bot": is_bot,
            "source_code": source_code,
        }
        # Удаляем ключи с None для чистоты
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 201:
                    logger.info(f"Новый пользователь {tg_id} успешно создан (201).")
                    return await response.json()
                elif response.status == 400:
                    error_detail = await response.json()
                    # Если пользователь уже существует, это нормально для /start логики
                    if 'tg_id' in error_detail and 'already exists' in str(error_detail['tg_id']):
                        logger.warning(f"Пользователь {tg_id} уже существует (400 Conflict).")
                        return {"tg_id": tg_id, "message": "User already exists (via add_user)."}

                    logger.error(
                        f"Ошибка API при add_user {tg_id}. Статус: 400. Детали: {error_detail}"
                    )
                    return None
                else:
                    error_detail = await response.json()
                    logger.error(
                        f"Ошибка API при add_user {tg_id}. Статус: {response.status}. Детали: {error_detail}"
                    )
                    return None

        except aiohttp.ClientConnectorError as e:
            logger.error(f"Ошибка подключения к API {url}: {e}")
            return None

    # --- 3. PATCH_USER (PATCH) ---
    async def patch_user(
            self,
            tg_id: int,
            payload: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Обновляет только переданные поля существующего пользователя.
        PATCH /api/v1/users/{tg_id}/
        """
        url = f"{self.base_url}/users/{tg_id}/"

        # Удаляем ключи с None из payload
        clean_payload = {k: v for k, v in payload.items() if v is not None}

        if not clean_payload:
            return None  # Нечего обновлять

        try:
            async with self.session.patch(url, json=clean_payload) as response:
                if response.status == 200:
                    logger.info(f"Пользователь {tg_id} успешно обновлен (200).")
                    return await response.json()
                elif response.status == 404:
                    logger.warning(f"Пользователь {tg_id} не найден для обновления (404).")
                    return None
                else:
                    error_detail = await response.json()
                    logger.error(
                        f"Ошибка API при PATCH {tg_id}. Статус: {response.status}. Детали: {error_detail}"
                    )
                    return None
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Ошибка подключения к API {url}: {e}")
            return None