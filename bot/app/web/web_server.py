import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config.settings import Settings


async def build_and_start_web_app(
    dp: Dispatcher,
    bot: Bot,
    settings: Settings,
):
    app = web.Application()

    # Прокидываем общие зависимости
    app["bot"] = bot
    app["dp"] = dp
    app["settings"] = settings

    # Инициализация webhook-обработки
    setup_application(app, dp, bot=bot)

    telegram_uses_webhook_mode = bool(settings.WEBHOOK_BASE_URL)
    if telegram_uses_webhook_mode:
        telegram_webhook_path = f"/{settings.BOT_TOKEN}"
        app.router.add_post(
            telegram_webhook_path,
            SimpleRequestHandler(dispatcher=dp, bot=bot),
        )
        logging.info(f"🌐 Telegram webhook route: [POST] {telegram_webhook_path}")

    # --- Health-check endpoint (по желанию)
    async def health_check(request: web.Request):
        return web.json_response({"status": "ok"})

    app.router.add_get("/health", health_check)

    web_app_runner = web.AppRunner(app)
    await web_app_runner.setup()
    site = web.TCPSite(
        web_app_runner,
        host=settings.WEB_SERVER_HOST,
        port=settings.WEB_SERVER_PORT,
    )

    await site.start()
    logging.info(
        f"✅ AIOHTTP сервер запущен: http://{settings.WEB_SERVER_HOST}:{settings.WEB_SERVER_PORT}"
    )

    # Настраиваем Telegram webhook
    if telegram_uses_webhook_mode:
        full_webhook_url = f"{settings.WEBHOOK_BASE_URL}/{settings.BOT_TOKEN}"
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(full_webhook_url)
        logging.info(f"🤖 Telegram webhook установлен: {full_webhook_url}")

    await asyncio.Event().wait()
