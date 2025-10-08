import logging
from aiogram import Bot, Dispatcher
from config.settings import Settings
from bot.routers import build_root_router
from bot.app.controllers.dispatcher_controller import build_dispatcher
from bot.app.web.web_server import build_and_start_web_app

# НОВЫЙ ИМПОРТ: Ваш сервис для работы с Django API
from api.user_service import UserService
from api.settings_service import SettingsService


async def register_all_routers(dp: Dispatcher, settings: Settings):
    # Роутеры будут иметь доступ к user_service через workflow_data
    dp.include_router(build_root_router(settings))
    logging.info("✅ Все роутеры успешно зарегистрированы.")


async def run_bot(settings_param: Settings):
    # 1. Инициализация UserService
    # Здесь предполагается, что settings_param содержит URL вашего Django API
    user_service = UserService(base_url=settings_param.BASE_URL_API)
    api_settings = SettingsService(base_url=settings_param.BASE_URL_API)

    dp, bot = build_dispatcher(settings_param)

    # 2. Добавление сервиса в данные диспетчера
    # Теперь UserService будет доступен в хэндлерах через аргумент user_service
    dp["user_service"] = user_service

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
        # 3. Закрытие сессии aiohttp при завершении работы бота
        logging.info("🔴 Закрытие aiohttp сессии UserService...")
        await user_service.close()
        await api_settings.close()

# ПРИМЕЧАНИЕ:
# Убедитесь, что вы добавили поле DJANGO_API_URL в ваш класс Settings
# (например, DJANGO_API_URL: str = 'http://localhost:8000/api/v1').