import aiohttp
from config.settings import Settings


class SettingsService:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = aiohttp.ClientSession()

    async def close(self):
        """Закрывает сессию aiohttp."""
        await self.session.close()

    async def get_settings(self):
        async with aiohttp.ClientSession() as session:

            async with session.get(f"{self.base_url}/settings/") as response:
                data = await response.json()
                # Возьмем первую запись
                if isinstance(data, list) and data:
                    return data[0]
                return data
