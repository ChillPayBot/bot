from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from bot.texts import PAYMENT_MENU


def get_payment_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    buttons += [
        InlineKeyboardButton(text=PAYMENT_MENU["payment_balance_button"], callback_data="payment_action:top_up"),
        InlineKeyboardButton(text=PAYMENT_MENU["payment_transactions_button"], callback_data="payment_action:transactions"),
        InlineKeyboardButton(text=PAYMENT_MENU["payment_methods_button"], callback_data="payment_action:methods"),
        InlineKeyboardButton(text=PAYMENT_MENU["payment_change_email_button"], callback_data="payment_action:change_email"),

        InlineKeyboardButton(text=PAYMENT_MENU["back_to_main_menu_button"], callback_data="payment_action:back_to_profile"),
    ]

    builder.add(*buttons)
    builder.adjust(1)

    return builder.as_markup()


def get_balance_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    buttons += [
        InlineKeyboardButton(text=PAYMENT_MENU["payment_choice_rub_button"], callback_data="payment_select_currency:choice_rub"),
        InlineKeyboardButton(text=PAYMENT_MENU["payment_choice_crypt_button"], callback_data="payment_select_currency:choice_crypt"),

        InlineKeyboardButton(text=PAYMENT_MENU["back_to_main_menu_button"], callback_data="payment_action:back_to_profile"),
    ]

    builder.add(*buttons)
    builder.adjust(1)

    return builder.as_markup()


def get_payment_button_inline_keyboard(url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    buttons += [
        InlineKeyboardButton(text=PAYMENT_MENU["payment_balance_pay_button"], url=url),

        InlineKeyboardButton(text=PAYMENT_MENU["back_to_main_menu_button"], callback_data="payment_action:back_to_profile"),
    ]

    builder.add(*buttons)
    builder.adjust(1)

    return builder.as_markup()