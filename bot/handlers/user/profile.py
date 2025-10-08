from aiogram import Router, types, F
from aiogram.utils.text_decorations import html_decoration as hd

from config.settings import Settings
from api.user_service import UserService
from bot.texts import PROFILE, PAYMENT_MENU
from bot.keyboards.inline.profile_keyboards import get_profile_inline_keyboard, get_payment_inline_keyboard
from .start import send_main_menu

router = Router(name="user_profile_router")


# Страница профиля
async def send_profile_menu(callback: types.CallbackQuery, user_service: UserService):
    user_id = callback.from_user.id
    user_data = await user_service.get_user_data(user_id)

    if not user_data:
        await callback.answer(PROFILE['profile_error_data_action'], show_alert=True)
        return

    username = hd.quote(user_data.get("username") or PROFILE["profile_data_not_set"])
    email = hd.quote(user_data.get("email") or PROFILE["profile_data_not_set"])
    balance = user_data.get("balance", 0.0)
    invited_friends = user_data.get("invited_friends", 0)
    active_subs = user_data.get("active_subs", 0)

    info_block = PROFILE["profile_info"].format(
        username=username,
        email=email,
        balance=f"{balance:,.2f}".replace(",", " "),
        invited_friends=invited_friends,
        active_subs=active_subs
    )

    text = f"{PROFILE['profile_title']}\n\n{info_block}"
    reply_markup = get_profile_inline_keyboard()

    if callback.message:
        await callback.message.edit_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode="html"
        )

        await callback.answer()


@router.callback_query(F.data == "main_action:profile")
async def show_profile_handler(callback: types.CallbackQuery, user_service: UserService):
    await send_profile_menu(callback, user_service)


@router.callback_query(F.data.startswith("profile_action:"))
async def profile_action_callback_handler(callback: types.CallbackQuery, settings: Settings, user_service: UserService):
    action = callback.data.split(":")[-1]

    if not callback.message:
        await callback.answer("Error message context lost.", show_alert=True)
        return

    if action == "balance":
        text = PAYMENT_MENU["payment_title"] + "\n\n" + PAYMENT_MENU["payment_info"]
        reply_markup = get_payment_inline_keyboard()

        if callback.message:
            await callback.message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode="html"
            )
            await callback.answer()

    elif action == "keys":
        await callback.answer("Переход в раздел: Мои ключи", show_alert=True)

    elif action == "promo":
        await callback.answer("Введите промокод:", show_alert=True)

    elif action == "back_to_main":
        await send_main_menu(callback, settings, user_service)

    else:
        await callback.answer(PROFILE["profile_unknown_action"], show_alert=True)
