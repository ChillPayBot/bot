from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from typing import Optional
from bot.texts import HELP, BUTTONS_TYPES


# Убедитесь, что эта функция использует переданную ссылку
def get_subscription_menu_keyboard(subscription_link: Optional[str] = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    if subscription_link:
        buttons.append(
            InlineKeyboardButton(text="🔗 Моя ссылка на подписку", url=subscription_link)
        )

    buttons.append(
        InlineKeyboardButton(text=HELP["how_to_connect_button"], callback_data="how_to_connect")
    )

    buttons.append(
        InlineKeyboardButton(text=BUTTONS_TYPES["back_to_main_menu_button"], callback_data="sub_action:back_to_main")
    )

    builder.add(*buttons)
    builder.adjust(1)
    return builder.as_markup()
