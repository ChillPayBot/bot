from aiogram import Router, types, F

from bot.keyboards.inline.profile_keyboards import get_payment_inline_keyboard

router = Router(name="user_payment_router")


@router.callback_query(F.data.startswith("profile_action:"))
async def payment_action_callback_handler(call: types.CallbackQuery):
    """
    Обрабатывает все нажатия кнопок внутри меню "Управление платежами".
    """
    action = call.data.split(":")[-1]

    if action == "top_up":
        await call.answer("Запуск процедуры пополнения баланса...", show_alert=True)
        # TODO: Логика FSM для пополнения

    elif action == "transactions":
        await call.answer("Загрузка истории транзакций...", show_alert=True)
        # TODO: Логика вывода списка

    elif action == "methods":
        await call.answer("Управление методами оплаты в разработке.", show_alert=True)

    elif action == "change_email":
        await call.answer("Пожалуйста, введите новый email.", show_alert=True)
        # TODO: Логика FSM для изменения email

    else:
        await call.answer("Неизвестное действие платежа", show_alert=True)
