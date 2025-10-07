from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from config.settings import Settings
from bot.texts import MAIN_MENU


def get_main_menu_inline_keyboard(settings: Settings, show_trial_button: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    if show_trial_button and settings.TRIAL_ENABLED:
        buttons.append(InlineKeyboardButton(
            text=MAIN_MENU["trial_button"],
            callback_data="main_action:request_trial"
        ))

    buttons += [
        InlineKeyboardButton(text=MAIN_MENU["buy_vpn"], callback_data="main_action:my_subscription"),
        InlineKeyboardButton(text=MAIN_MENU["profile"], callback_data="main_action:profile"),
        InlineKeyboardButton(text=MAIN_MENU["how_to_connect"], callback_data="main_action:subscribe"),
        InlineKeyboardButton(text=MAIN_MENU["referral"], callback_data="main_action:referral"),
        InlineKeyboardButton(text=MAIN_MENU["support"], callback_data="main_action:support")
    ]

    builder.add(*buttons)
    builder.adjust(1, 2, 1)

    return builder.as_markup()
