from pathlib import Path
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.text_decorations import html_decoration as hd
from aiogram.types import FSInputFile
from typing import Union

from config.settings import Settings
from bot.texts import MAIN_MENU
from bot.keyboards.inline.user_keyboards import get_main_menu_inline_keyboard
from bot.utils.messages import edit_or_send_message

from api.settings_service import SettingsService
from api.user_service import UserService
from api.tariff_service import TariffAPIService


router = Router(name="user_start_router")

IMAGE_PATH = Path('img') / 'menu.jpg'


async def send_main_menu(callback: types.CallbackQuery,
                         settings: Settings,
                         user_service: UserService):
    user = callback.from_user
    user_data = await user_service.get_user_data(user.id)

    if not user_data:
        user_data = await user_service.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            language_code=user.language_code
        )
    else:
        await user_service.patch_user(user.id, {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name
        })

    if not user_data:
        await callback.answer("Ошибка при создании профиля. Попробуйте позже.")
        return

    show_trial_button = not user_data.get('trial_used', True)

    text = MAIN_MENU["main_menu_greeting"]
    main_keyboard = get_main_menu_inline_keyboard(settings, show_trial_button)

    await edit_or_send_message(
        target_event=callback,
        text=text,
        reply_markup=main_keyboard,
        media_path=IMAGE_PATH
    )


@router.message(CommandStart())
async def start_command_handler(message: types.Message, settings: Settings, user_service: UserService):
    await send_main_menu(message, settings, user_service)


@router.callback_query(F.data.startswith("main_action:"))
async def profile_action_callback_handler(callback: types.CallbackQuery, settings: Settings, user_service: UserService, tariff_service: TariffAPIService):
    action = callback.data.split(":")[-1]

    if not callback.message:
        await callback.answer("Error message context lost.", show_alert=True)
        return

    if action == "sub":
        from .subscription import send_user_subscription_menu
        await send_user_subscription_menu(callback, user_service)

    elif action == "request_trial":
        from .trial import request_trial_handler
        await request_trial_handler(callback)

    elif action == "buy_subscription":
        from .tariffs import send_tariffs_menu
        await send_tariffs_menu(callback, settings, user_service, tariff_service)

    elif action == "promo":
        await callback.answer("Введите промокод:", show_alert=True)

    elif action == "back_to_main":
        await send_main_menu(callback, settings, user_service)

    else:
        await callback.answer(MAIN_MENU["main_menu_unknown_action"], show_alert=True)
