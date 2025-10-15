from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from config.settings import Settings

from bot.texts import BUTTONS_TYPES, HELP


def get_trial_confirmation_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=BUTTONS_TYPES["activate_button"],
            callback_data="trial:confirm"
        ),
        InlineKeyboardButton(
            text=BUTTONS_TYPES["cancel_button"],
            callback_data="back_to_main"
        )
    )
    return builder.as_markup()


def get_trial_success_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=HELP["how_to_connect_button"],
            callback_data="show_connection_guide"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=BUTTONS_TYPES["back_to_main_menu_button"],
            callback_data="back_to_main"
        )
    )
    return builder.as_markup()