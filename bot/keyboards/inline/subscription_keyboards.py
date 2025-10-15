from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from config.settings import Settings
from typing import Optional

from bot.texts import HELP, BUTTONS_TYPES


def get_subscription_menu_keyboard(subscription_link: Optional[str] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    buttons += [
        InlineKeyboardButton(text=HELP["how_to_connect_button"], url=subscription_link),
        InlineKeyboardButton(text=BUTTONS_TYPES["back_to_main_menu_button"], callback_data="sub_action:back_to_main")
    ]

    builder.add(*buttons)
    builder.adjust(1)
    return builder.as_markup()
