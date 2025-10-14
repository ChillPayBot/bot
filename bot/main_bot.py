import logging
import aiohttp
from aiogram import Bot, Dispatcher
from config.settings import Settings
from bot.routers import build_root_router
from bot.app.controllers.dispatcher_controller import build_dispatcher
from bot.app.web.web_server import build_and_start_web_app

from api.user_service import UserService
from api.settings_service import SettingsService
from api.subscription_service import SubscriptionAPIService
from api.tariff_service import TariffAPIService

ServiceContainer = dict[str, UserService | SettingsService]


# Настройки для сессии (заголовки, токены)
def _get_api_headers(token: str) -> dict:
    return {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }


async def on_startup(dispatcher: Dispatcher, settings: Settings):
    API_BASE_URL = settings.API_BASE_URL.rstrip('/') + '/api/v1'
    API_TOKEN = settings.API_TOKEN

    session = aiohttp.ClientSession(headers=_get_api_headers(API_TOKEN))

    user_service = UserService(base_url=API_BASE_URL, session=session)
    subscription_service = SubscriptionAPIService(base_url=API_BASE_URL, session=session)
    tariff_service = TariffAPIService(base_url=API_BASE_URL, session=session)


    dispatcher["user_service"] = user_service
    dispatcher["sub_api_service"] = subscription_service
    dispatcher["tariff_service"] = tariff_service
    dispatcher["aiohttp_session"] = session

    logging.info("✅ Асинхронные сервисы и сессия aiohttp инициализированы.")


async def on_shutdown(dispatcher: Dispatcher):
    """Корректное закрытие асинхронной сессии при завершении работы бота."""
    session = dispatcher.get("aiohttp_session")
    if session:
        await session.close()
        logging.info("🔴 Сессия aiohttp успешно закрыта.")


async def register_all_routers(dp: Dispatcher, settings: Settings):
    dp.include_router(build_root_router(settings))
    logging.info("✅ Все роутеры успешно зарегистрированы.")


async def run_bot(settings_param: Settings):
    # 1. Инициализация диспетчера и бота
    dp, bot = build_dispatcher(settings_param)

    # 2. РЕГИСТРАЦИЯ ХЕНДЛЕРОВ ЖИЗНЕННОГО ЦИКЛА
    # Регистрируем функцию, которая инициализирует сервисы
    dp.startup.register(on_startup)
    # Регистрируем функцию, которая закрывает сессию
    dp.shutdown.register(on_shutdown)

    # 3. Регистрация роутеров
    await register_all_routers(dp, settings_param)

    try:
        if settings_param.DEBUG or not settings_param.WEBHOOK_BASE_URL:
            logging.info("🧩 Запуск бота в режиме polling (DEBUG=True)")
            await bot.delete_webhook(drop_pending_updates=True)
            # Вся магия инициализации произойдет до dp.start_polling
            await dp.start_polling(bot)

        else:
            logging.info("🚀 Запуск webhook сервера...")
            await build_and_start_web_app(dp, bot, settings_param)

    finally:
        logging.info("🔴 Завершение работы бота.")