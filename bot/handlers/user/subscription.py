import logging
from datetime import datetime
from pathlib import Path
from aiogram import Router, types, F

from config.settings import Settings

from api.user_service import UserService

from bot.texts import SUBSCRIPTION_MENU
from bot.keyboards.inline.subscription_keyboards import get_subscription_menu_keyboard
from bot.utils.messages import edit_or_send_message

logger = logging.getLogger(__name__)
router = Router(name="user_subscription_router")
IMAGE_PATH = Path('img') / 'tarifss.jpg'


async def send_user_subscription_menu(callback: types.CallbackQuery, user_service: UserService):
    """Отправляет меню с активной подпиской пользователя."""

    await callback.answer("Загрузка подписок...")

    user_id = callback.from_user.id

    current_sub = await user_service.get_current_subscription(user_id)

    text_parts = [SUBSCRIPTION_MENU["sub_title"]]

    # 💡 ИСПРАВЛЕНИЕ: Инициализация переменной здесь
    subscription_link_to_button = None

    if current_sub is None:
        text_parts.append(SUBSCRIPTION_MENU["no_active_subs"])

    else:
        is_trial = current_sub.get('trial_used', False)

        if is_trial:
            tariff_display_name = "Пробный период (Trial)"
        else:
            tariff_display_name = current_sub.get('tariff_name', 'Неизвестный тариф')

        expires_at_str = current_sub.get('end_date')

        if expires_at_str:
            expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00')).strftime("%d.%m.%Y %H:%M")
        else:
            expires_at = "Бессрочно"

        # 1. Извлекаем ссылку
        subscription_link_to_text = current_sub.get('subscriptionUrl', 'Недоступна')

        # 2. Сохраняем ссылку для кнопки (если она есть)
        if subscription_link_to_text != 'Недоступна':
            subscription_link_to_button = subscription_link_to_text

        sub_block = SUBSCRIPTION_MENU["subscription_block_template"].format(
            tariff_display_name=tariff_display_name,
            expires_at=expires_at,
            subscription_link=subscription_link_to_text
        )

        text_parts.append(f"<blockquote>{sub_block}</blockquote>")

    final_text = "\n\n".join(text_parts)

    # Переменная теперь всегда существует и равна None, если подписки нет.
    reply_markup = get_subscription_menu_keyboard(subscription_link=subscription_link_to_button)

    await edit_or_send_message(
        target_event=callback,
        text=final_text,
        reply_markup=reply_markup,
        media_path=IMAGE_PATH
    )


@router.callback_query(F.data.startswith("sub_action:"))
async def subscription_action_callback_handler(callback: types.CallbackQuery, settings: Settings, user_service: UserService):
    action = callback.data.split(":")[-1]

    if not callback.message:
        await callback.answer("Error message context lost.", show_alert=True)
        return

    if action == "back_to_main":
        from .start import send_main_menu

        await send_main_menu(callback, settings, user_service)

    else:
        await callback.answer(PROFILE["profile_unknown_action"], show_alert=True)