from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from config.settings import Settings

from bot.texts import MAIN_MENU, TRIAL, TARIFF_ICONS, HELP


def get_main_menu_inline_keyboard(settings: Settings, show_trial_button: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    if show_trial_button and settings.TRIAL_ENABLED:
        buttons.append(InlineKeyboardButton(
            text=MAIN_MENU["menu_activate_trial_button"],
            callback_data="main_action:request_trial"
        ))

    buttons += [
        InlineKeyboardButton(text=MAIN_MENU["menu_subscribe_inline"], callback_data="main_action:buy_subscription"),
        InlineKeyboardButton(text=MAIN_MENU["menu_my_sub_inline"], callback_data="main_action:sub"),
        InlineKeyboardButton(text=HELP["how_to_connect_button"], callback_data="main_action:subscribe"),
        InlineKeyboardButton(text=MAIN_MENU["menu_apply_promo_button"], callback_data="main_action:referral"),
        InlineKeyboardButton(text=HELP["not_work_vpn_button"], callback_data="main_action:support")
    ]

    builder.add(*buttons)
    builder.adjust(1, 2, 1)

    return builder.as_markup()




