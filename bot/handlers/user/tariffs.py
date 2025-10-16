import logging
from pathlib import Path
from aiogram import Router, types, F
from config.settings import Settings

from api.user_service import UserService
from api.tariff_service import TariffAPIService

from bot.keyboards.inline.tariffs_keyboards import get_tariffs_keyboard
from bot.utils.messages import edit_or_send_message
from bot.texts import TARIFFS, TARIFF_ICONS
from .start import send_main_menu

logger = logging.getLogger(__name__)

router = Router(name="user_buy_router")

IMAGE_PATH = Path('img') / 'tarifss.jpg'


async def send_tariffs_menu(callback: types.CallbackQuery, settings: Settings, user_service: UserService,
                            tariff_service: TariffAPIService):
    """Отправляет меню с активными тарифами."""

    await callback.answer("Загрузка тарифов...")

    tariffs = await tariff_service.get_active_tariffs()

    if tariffs is None:
        await edit_or_send_message(
            target_event=callback,
            text=TARIFFS["error_loading_tariffs"],
            reply_markup=get_tariffs_keyboard([])
        )
        await callback.answer(TARIFFS["error_loading_tariffs"], show_alert=True)
        return

    if not tariffs:
        await edit_or_send_message(
            target_event=callback,
            text=TARIFFS["no_tariffs_available"],
            reply_markup=get_tariffs_keyboard([])
        )
        return

    text_parts = [TARIFFS["tariff_menu_header"]]

    for tariff in tariffs:
        icon = TARIFF_ICONS.get(tariff['slug'], TARIFF_ICONS['default'])

        tariff_header = TARIFFS["tariff_header_template"].format(icon=icon, name=tariff['name'])

        tariff_content = TARIFFS["tariff_content_template"].format(
            devices_limit=tariff['devices_limit'],
            price=f"{float(tariff['price_per_month']):.2f}"
        )

        tariff_block = (
            f"{tariff_header}\n"
            f"<blockquote>{tariff_content}</blockquote>"
        )

        text_parts.append(tariff_block)

    final_text = "\n\n".join(text_parts)

    await edit_or_send_message(
        target_event=callback,
        text=final_text,
        reply_markup=get_tariffs_keyboard(tariffs),
        media_path=IMAGE_PATH
    )


# ----------------- Хендлеры -----------------

@router.callback_query(F.data == "main_action:buy_subscription")
async def handle_buy_subscription(
        callback: types.CallbackQuery,
        settings: Settings,
        user_service: UserService,
        tariff_service: TariffAPIService
):
    """Обрабатывает нажатие на кнопку 'Купить подписку'."""
    await send_tariffs_menu(callback, settings, user_service, tariff_service)


@router.callback_query(F.data.startswith("tariff_action:"))
async def tariffs_action_callback_handler(callback: types.CallbackQuery, settings: Settings, user_service: UserService):
    action = callback.data.split(":")[-1]

    if not callback.message:
        await callback.answer("Error message context lost.", show_alert=True)
        return

    if action == "back_to_main":
        from .start import send_main_menu

        await send_main_menu(callback, settings, user_service)

    else:
        await callback.answer(PROFILE["profile_unknown_action"], show_alert=True)
