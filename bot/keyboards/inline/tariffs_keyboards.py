from typing import Optional, Dict, Any, List
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from bot.texts import TARIFF_ICONS


def get_tariffs_keyboard(tariffs: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    """Генерирует инлайн-клавиатуру для выбора тарифа."""
    builder = InlineKeyboardBuilder()

    for tariff in tariffs:
        icon = TARIFF_ICONS.get(tariff['slug'], TARIFF_ICONS['default'])

        text = f"{icon} {tariff['name']}"

        callback_data = f"tariff:select:{tariff['slug']}"

        builder.row(InlineKeyboardButton(text=text, callback_data=callback_data))

    builder.adjust(1)
    return builder.as_markup()
