import logging
from aiogram import Router, types, F
from config.settings import Settings
from api.user_service import UserService
from api.subscription_service import SubscriptionAPIService

from bot.texts import TRIAL
from bot.keyboards.inline.trial_keyboards import get_trial_confirmation_keyboard, get_trial_success_keyboard
from bot.utils.messages import edit_or_send_message

from .start import send_main_menu

logger = logging.getLogger(__name__)

router = Router(name="user_trial_router")


async def request_trial_handler(callback: types.CallbackQuery):
    await edit_or_send_message(
        target_event=callback,
        text=TRIAL["trial_confirmation_text"],
        reply_markup=get_trial_confirmation_keyboard(),
    )


@router.callback_query(F.data == "trial:confirm")
async def confirm_trial_handler(callback: types.CallbackQuery, user_service: UserService,
                                sub_api_service: SubscriptionAPIService, settings: Settings):
    user_telegram_id = callback.from_user.id
    await callback.answer("Активируем пробный период...")

    response = await sub_api_service.activate_trial(user_telegram_id)

    if response and not response.get("error"):

        connection_link = response.get("subscriptionUrl")
        trial_duration = response.get("trial_days")

        if connection_link and trial_duration is not None:

            success_text = TRIAL["trial_success_message"].format(
                duration=trial_duration,
                connection_link=connection_link
            )

            await edit_or_send_message(
                target_event=callback,
                text=success_text,
                reply_markup=get_trial_success_keyboard(),
            )
        else:
            logger.error(f"API returned success but missing link/duration. Response: {response}")
            await callback.answer("Ошибка: сервер не предоставил ссылку для подключения.", show_alert=True)
            await send_main_menu(callback, settings, user_service)

    elif response and response.get("error"):
        error_message = response["error"]
        logger.warning(f"Trial activation failed for {user_telegram_id}. Error: {error_message}")
        await callback.answer(error_message, show_alert=True)
        await send_main_menu(callback, settings, user_service)

    else:
        await callback.answer("Не удалось активировать пробный период. Попробуйте позже.", show_alert=True)
        await send_main_menu(callback, settings, user_service)
