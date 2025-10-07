import aiohttp
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class UserService:
    """
    Сервис для взаимодействия с REST API Django по сущности User.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = aiohttp.ClientSession()
        logger.info(f"UserService инициализирован с базовым URL: {self.base_url}")

    async def close(self):
        """Закрывает сессию aiohttp."""
        await self.session.close()

    async def upsert_user(
            self,
            tg_id: int,
            username: Optional[str] = None,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            language_code: Optional[str] = None,
            is_bot: bool = False,
            source_code: Optional[str] = None,
            only_if_exists: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Регистрирует или обновляет пользователя в Django API.
        Соответствует вашему методу upsert_user и POST /api/v1/users/.
        """
        url = f"{self.base_url}/users/"

        # Подготавливаем данные, исключая None, кроме тех, которые могут быть None в БД
        payload = {
            "tg_id": tg_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "language_code": language_code,
            "is_bot": is_bot,
            "source_code": source_code,
            "only_if_exists": only_if_exists,
        }
        # Удаляем ключи с None для более чистого запроса, кроме тех,
        # которые явно могут быть None (включая username, first_name и т.д.)
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            async with self.session.post(url, json=payload) as response:

                if response.status == 201:
                    # Успешное создание или обновление
                    return await response.json()

                elif response.status == 404 and only_if_exists:
                    # Пользователь не найден при only_if_exists=True
                    logger.warning(f"Пользователь {tg_id} не найден при попытке обновления.")
                    return None

                else:
                    error_detail = await response.json()
                    logger.error(
                        f"Ошибка API при upsert_user {tg_id}. Статус: {response.status}. "
                        f"Детали: {error_detail}"
                    )
                    # Можно поднять исключение или вернуть None
                    return None

        except aiohttp.ClientConnectorError as e:
            logger.error(f"Ошибка подключения к API {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Неизвестная ошибка при запросе к API: {e}")
            return None