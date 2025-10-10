from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from bot.keyboards.inline.payment_keyboards import get_balance_inline_keyboard, get_payment_button_inline_keyboard
from bot.states.user_states import PaymentStates
from api.user_service import UserService
from api.settings_service import SettingsService

router = Router(name="user_payment_router")


@router.callback_query(F.data.startswith("payment_action:"))
async def payment_action_callback_handler(callback: types.CallbackQuery, user_service: UserService):
    action = callback.data.split(":")[-1]

    if action == "top_up":
        text = "Выберите метод оплаты"
        reply_markup = get_balance_inline_keyboard()

        if callback.message:
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="html"
            )
            await callback.answer()

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


@router.callback_query(F.data.startswith("payment_select_currency:"))
async def select_currency_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    currency = callback.data.split(":")[-1]

    await state.update_data(chosen_currency=currency)

    await state.set_state(PaymentStates.waiting_for_amount)

    text = f"Введите сумму пополнения:"

    if callback.message:
        await callback.message.edit_text(
            text=text,
            reply_markup=None,  # Убираем клавиатуру после выбора
            parse_mode="html"
        )
        await callback.answer()


@router.message(PaymentStates.waiting_for_amount)
async def process_payment_amount(message: types.Message, state: FSMContext, api_settings: SettingsService):
    global_settings = await api_settings.get_global_settings()
    min_amount = global_settings.get('min_top_up_amount', 100)

    # 2. Валидация
    if not message.text or not message.text.isdigit() or int(message.text) < min_amount:
        await message.answer(f"❌ Минимальная сумма пополнения баланса от {min_amount}₽")
        return

    data = await state.get_data()

    payment_url = f"https://tg.com/"

    await message.answer(
        text=f"💳 Пополнение баланса",
        reply_markup=get_payment_button_inline_keyboard(payment_url),
        parse_mode="html"
    )

    await state.clear()
