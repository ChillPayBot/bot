from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from bot.texts import PROFILE


def get_profile_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    buttons += [
        InlineKeyboardButton(text=PROFILE["profile_my_balance_button"], callback_data="profile_action:balance"),
        InlineKeyboardButton(text=PROFILE["profile_my_keys_button"], callback_data="profile_action:keys"),
        InlineKeyboardButton(text=PROFILE["profile_activate_promocode_button"], callback_data="profile_action:promo"),

        InlineKeyboardButton(text=PROFILE["back_to_main_menu_button"], callback_data="profile_action:back_to_main"),
    ]

    builder.add(*buttons)
    builder.adjust(1)

    return builder.as_markup()

