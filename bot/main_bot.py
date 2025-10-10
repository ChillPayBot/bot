import logging
from aiogram import Bot, Dispatcher
from config.settings import Settings
from bot.routers import build_root_router
from bot.app.controllers.dispatcher_controller import build_dispatcher
from bot.app.web.web_server import build_and_start_web_app

from api.user_service import UserService
from api.settings_service import SettingsService

ServiceContainer = dict[str, UserService | SettingsService]


def init_services(base_url_api: str, api_token: str) -> ServiceContainer:
    return {
        "user_service": UserService(base_url=base_url_api, api_token=api_token),
        "api_settings": SettingsService(base_url=base_url_api, api_token=api_token),
    }


async def register_all_routers(dp: Dispatcher, settings: Settings):
    dp.include_router(build_root_router(settings))
    logging.info("✅ Все роутеры успешно зарегистрированы.")


async def run_bot(settings_param: Settings):
    services = init_services(settings_param.BASE_URL_API, settings_param.BASE_API_TOKEN)

    dp, bot = build_dispatcher(settings_param)

    for key, service_instance in services.items():
        dp[key] = service_instance

    await register_all_routers(dp, settings_param)

    try:
        if settings_param.DEBUG or not settings_param.WEBHOOK_BASE_URL:
            logging.info("🧩 Запуск бота в режиме polling (DEBUG=True)")
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)

        else:
            logging.info("🚀 Запуск webhook сервера...")
            await build_and_start_web_app(dp, bot, settings_param)

    finally:
        logging.info("🔴 Завершение работы бота.")