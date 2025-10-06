from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard():
    """
    Главное меню бота с кнопками
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Моя подписка", callback_data="main_action:my_subscription"),
            InlineKeyboardButton(text="Купить / Продлить", callback_data="main_action:subscribe")
        ],
        [
            InlineKeyboardButton(text="Помощь", callback_data="main_action:help")
        ]
    ])
    return keyboard
