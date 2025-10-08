from aiogram import Router, types, F

from bot.keyboards.inline.profile_keyboards import get_payment_inline_keyboard
from bot.handlers.user.profile import send_profile_menu
from api.user_service import UserService

router = Router(name="user_payment_router")


@router.callback_query(F.data.startswith("payment_action:"))
async def payment_action_callback_handler(callback: types.CallbackQuery, user_service: UserService):
    action = callback.data.split(":")[-1]

    if action == "top_up":
        await callback.answer("Запуск процедуры пополнения баланса...", show_alert=True)

    elif action == "transactions":
        await callback.answer("Загрузка истории транзакций...", show_alert=True)

    elif action == "methods":
        await callback.answer("Управление методами оплаты в разработке.", show_alert=True)

    elif action == "change_email":
        await callback.answer("Пожалуйста, введите новый email.", show_alert=True)

    elif action == "back_to_profile":
        await send_profile_menu(callback, user_service)

    else:
        await callback.answer("Неизвестное действие платежа", show_alert=True)
