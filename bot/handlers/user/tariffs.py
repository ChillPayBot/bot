import logging
from aiogram import Router, types, F
from config.settings import Settings
from api.user_service import UserService
from api.tariff_service import TariffAPIService  # <--- Новый сервис
from bot.keyboards.inline.user_keyboards import get_tariffs_keyboard
from bot.texts import TARIFFS
from .start import send_main_menu

logger = logging.getLogger(__name__)

router = Router(name="user_buy_router")


async def send_tariffs_menu(callback: types.CallbackQuery, settings: Settings, user_service: UserService, tariff_service: TariffAPIService):
    """Отправляет меню с активными тарифами."""

    await callback.answer("Загрузка тарифов...")

    # 1. Получаем список тарифов из API
    tariffs = await tariff_service.get_active_tariffs()

    if tariffs is None:
        # Ошибка подключения/API (возвращено None)
        await callback.message.edit_text(
            TARIFFS["error_loading_tariffs"],
            reply_markup=get_tariffs_keyboard([])  # Пустая клавиатура с кнопкой "назад"
        )
        await callback.answer(TARIFFS["error_loading_tariffs"], show_alert=True)
        return

    if not tariffs:
        # Тарифы не найдены (возвращен пустой список)
        await callback.message.edit_text(
            TARIFFS["no_tariffs_available"],
            reply_markup=get_tariffs_keyboard([])
        )
        return

    # 2. Формируем клавиатуру и текст
    text = TARIFFS["choose_tariff_message"]
    reply_markup = get_tariffs_keyboard(tariffs)

    # 3. Отправляем пользователю
    await callback.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


# ----------------- Хендлеры -----------------

@router.callback_query(F.data == "main_action:buy_subscription")
async def handle_buy_subscription(
        callback: types.CallbackQuery,
        settings: Settings,
        user_service: UserService,
        tariff_service: TariffAPIService  # <--- Используем новый сервис
):
    """Обрабатывает нажатие на кнопку 'Купить подписку'."""
    await send_tariffs_menu(callback, settings, user_service, tariff_service)

# TODO: Добавить хендлер для обработки выбора тарифа:
# @router.callback_query(F.data.startswith("tariff:select:"))
# async def handle_tariff_selection(...):
#     tariff_slug = callback.data.split(":")[-1]
#     # ... логика выбора продолжительности и оплаты ...