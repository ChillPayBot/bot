from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.text_decorations import html_decoration as hd
from typing import Union

from config.settings import Settings
from bot.keyboards.inline.user_keyboards import get_main_menu_inline_keyboard
from api.user_service import UserService
from bot.texts import MAIN_MENU

router = Router(name="user_start_router")

# Временно хранение статуса пробного периода
trial_status_memory: dict[int, bool] = {}


def can_user_use_trial(user_id: int) -> bool:
    return trial_status_memory.get(user_id, True)


# handlers/user/start.py (Обновленный код)

# ... (Существующие импорты и код) ...

async def send_main_menu(target_event: Union[types.Message, types.CallbackQuery],
                         settings: Settings,
                         user_service: UserService,
                         user_data: dict | None = None):
    user = target_event.from_user

    # 1. Извлечение данных пользователя
    # Поскольку user_data формируется тут же, мы можем передать данные напрямую.
    # Если target_event — это CallbackQuery, нам нужно брать данные из event.from_user.

    payload = {
        "tg_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
        "is_bot": user.is_bot,
        # 'source_code' можно добавить здесь, если он извлекается из команды /start
    }

    await user_service.upsert_user(
        **payload,
        only_if_exists=False
    )

    user_id = user.id

    show_trial_button_in_menu = can_user_use_trial(user_id)

    text = MAIN_MENU["main_menu_greeting"]
    reply_markup = get_main_menu_inline_keyboard(settings, show_trial_button_in_menu)

    if isinstance(target_event, types.Message):
        await target_event.answer(text, reply_markup=reply_markup)
    elif isinstance(target_event, types.CallbackQuery) and target_event.message:
        await target_event.message.edit_text(text, reply_markup=reply_markup)
        await target_event.answer()
    else:
        # на всякий случай
        print(f"Не удалось отправить меню для пользователя {user_id}")


@router.message(CommandStart())
async def start_command_handler(message: types.Message, settings: Settings, user_service: UserService):
    await send_main_menu(message, settings, user_service)
