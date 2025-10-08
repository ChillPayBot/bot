from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.text_decorations import html_decoration as hd
from typing import Union

from config.settings import Settings
from bot.keyboards.inline.user_keyboards import get_main_menu_inline_keyboard
from api.settings_service import SettingsService
from api.user_service import UserService
from bot.texts import MAIN_MENU

router = Router(name="user_start_router")

# Временно хранение статуса пробного периода
trial_status_memory: dict[int, bool] = {}


def can_user_use_trial(user_id: int) -> bool:
    return trial_status_memory.get(user_id, True)


async def send_main_menu(target_event: Union[types.Message, types.CallbackQuery],
                         settings: Settings,
                         user_service: UserService):
    user = target_event.from_user

    user_payload = {
        "tg_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
        "is_bot": user.is_bot,
    }

    existing_user_data = await user_service.get_user_data(user.id)

    if existing_user_data:
        # Пользователь существует: обновляем его данные (например, username)
        await user_service.patch_user(user.id, user_payload)

    else:
        # Пользователь не существует: создаем нового
        await user_service.add_user(
            **user_payload,
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


@router.message(CommandStart())
async def start_command_handler(message: types.Message, settings: Settings, user_service: UserService):
    await send_main_menu(message, settings, user_service)
