from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from bot.texts import PROFILE, PAYMENT_MENU


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


def get_payment_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    buttons += [
        InlineKeyboardButton(text=PROFILE["payment_balance_button"], callback_data="payment_action:top_up"),
        InlineKeyboardButton(text=PROFILE["payment_transactions_button"], callback_data="payment_action:transactions"),
        InlineKeyboardButton(text=PROFILE["payment_methods_button"], callback_data="payment_action:methods"),
        InlineKeyboardButton(text=PROFILE["payment_change_email_button"], callback_data="payment_action:change_email"),

        InlineKeyboardButton(text=PROFILE["back_to_main_menu_button"], callback_data="payment_action:back_to_main"),
    ]

    builder.add(*buttons)
    builder.adjust(1, 2, 1)

    return builder.as_markup()