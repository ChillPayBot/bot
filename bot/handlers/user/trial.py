from aiogram import Router, types, F
from config.settings import Settings
from api.user_service import UserService
from .start import send_main_menu
from bot.keyboards.inline.user_keyboards import  get_trial_confirmation_keyboard, get_trial_success_keyboard
from bot.texts import TRIAL

router = Router(name="user_trial_router")

TRIAL_PERIOD_DAYS = 3


async def request_trial_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text=TRIAL["trial_confirmation_text"],
        reply_markup=get_trial_confirmation_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "trial:confirm")
async def confirm_trial_handler(callback: types.CallbackQuery, user_service: UserService, settings: Settings):
    user_telegram_id = callback.from_user.id
    await callback.answer("Активируем пробный период...")

    response = await user_service.activate_trial(user_telegram_id)

    if response and not response.get("error"):

        connection_link = response.get("subscription_link")
        trial_duration = response.get("trial_days")

        if connection_link and trial_duration is not None:
            # 3. Формируем текст успеха
            success_text = TRIAL["trial_success_message"].format(
                duration=trial_duration,
                connection_link=connection_link
            )

            await callback.message.edit_text(
                text=success_text,
                reply_markup=get_trial_success_keyboard(),
                parse_mode="HTML"
            )
        else:
            logger.error(f"API returned success but missing link/duration. Response: {response}")
            await callback.answer("Ошибка: сервер не предоставил ссылку для подключения.", show_alert=True)
            await send_main_menu(callback, settings, user_service)

    elif response and response.get("detail"):
        error_message = response["detail"]
        logger.warning(f"Trial activation failed for {user_telegram_id}. Error: {error_message}")
        await callback.answer(error_message, show_alert=True)
        await send_main_menu(callback, settings, user_service)

    else:
        # Непредвиденная ошибка
        await callback.answer("Не удалось активировать пробный период. Попробуйте позже.", show_alert=True)
        await send_main_menu(callback, settings, user_service)