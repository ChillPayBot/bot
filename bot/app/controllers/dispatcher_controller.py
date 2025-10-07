import logging
from typing import Dict, Tuple

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import Settings


def build_dispatcher(settings: Settings) -> tuple[Dispatcher, Bot]:
    storage = MemoryStorage()
    default_props = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=settings.BOT_TOKEN, default=default_props)

    dp = Dispatcher(storage=storage, settings=settings, bot_instance=bot)

    return dp, bot
