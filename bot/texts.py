MAIN_MENU = {
    "main_menu_greeting": "👋 Добро пожаловать в главное меню!\n\n🚀 Обходите блокировки, получайте доступ к любимому контенту и наслаждайтесь быстрой скоростью соединения.\n\n📖️ Выберите действие:",
    "menu_activate_trial_button": "🆓 Пробный период",
    "menu_subscribe_inline": "🌐 Купить VPN",
    "menu_my_sub_inline": "👤 Моя подписка",
    "menu_apply_promo_button": "🤝 Пригласить друзей",

    "main_menu_unknown_action": "Неизвестное действие.",
}


HELP = {
    "how_to_connect_button": "📖 Как подключить?",
    "not_work_vpn_button": "🆘 Не работает VPN?",
}

BUTTONS_TYPES = {
    "back_to_main_menu_button": "⬅️ Назад в главное меню",
    "activate_button": "✅ Активировать",
    "disable_button": "❌ Выключить",
    "cancel_button": "❌ Отмена",
}


SUBSCRIPTION_MENU = {
    "sub_title": "🌟 <b>Мои активные подписки</b>",
    "no_active_subs": "У вас нет активных подписок. Выберите тариф, чтобы начать пользоваться VPN.",
    "subscription_block_template": (
        "🔗 <b>Текущий тариф: {tariff_display_name}</b> 🔗\n\n"
        "   <b>Действует до: {expires_at} </b> \n"
        "   <b>Ссылка подписки: {subscription_link} </b> \n"
    ),
    "traffic_unlimited": "Безлимитный",
    "traffic_remaining": "{remaining_traffic} / {total_traffic}",


}

TARIFF_ICONS = {
    "basic": "🔘",
    "max": "🧩",
    "pro": "⭐️",
    "default": "🔹"
}

TARIFFS = {
    "tariff_menu_header": "<b>Выберите подходящий тариф ⤵️</b>",


    "tariff_header_template": "{icon} <b>{name}</b>",

    "tariff_content_template": (
        "- устройств: {devices_limit}\n"
        "- цена: {price} ₽/мес"
    ),

    "tariff_select_button": "{name} — {price}₽/мес",
    "no_tariffs_available": "К сожалению, сейчас нет доступных тарифов. Попробуйте позже.",
    "error_loading_tariffs": "Произошла ошибка при загрузке тарифов. Пожалуйста, попробуйте еще раз.",
}


TRIAL = {
    "trial_confirmation_text": (
        "Вы собираетесь активировать бесплатный пробный период.\n\n"
        "⏳ <b>Срок действия:</b> 7 дней\n\n"
        "Вы получите полный доступ ко всем возможностям VPN. Продолжить?"
    ),
    "trial_success_message": (
        "✅ <b>Бесплатная подписка успешно активирована!</b>\n\n"
        "⏱️ <b>Срок действия:</b> {duration} дней\n\n"
        "📝 <b>Данные для подключения:</b>\n"
        "Ссылка для подключения:\n"
        "`{connection_link}`"
    ),

    "trial_confirm_activate_button": "✅ Активировать",

}

PROFILE = {
    "profile_title": "<b>👤 Мой профиль </b>",
    "profile_info": (
        "👥 Пользователь: @{username}\n"
        "💳 Email: {email}\n"
        "💰 Баланс: {balance}₽\n"
        "🤝 Приглашено друзей: {invited_friends}\n"
        "🔑 Активных подписок: {active_subs}"
    ),

    "profile_my_balance_button": "💰 Мой баланс",
    "profile_my_keys_button": "🔑 Мои подписки",
    "profile_activate_promocode_button": "🎁 Активировать промокод",

    "back_to_main_menu_button": "⬅️ Назад",
    "profile_unknown_action": "Неизвестное действие.",
    "profile_error_data_action": "Не удалось загрузить данные профиля. Попробуйте снова.",
    "profile_data_not_set": "Данные отсутствуют",
}


PAYMENT_MENU = {
    "payment_title": "<b>💳 Управление платежами </b>",
    "payment_info": (
        "Здесь вы можете:\n\n"
        "• 💰 Пополнить баланс - внести средства на счёт\n"
        "• 💳 Мои транзакции - посмотреть историю транзакций\n"
        "• ⚙️ Методы оплаты - управлять методами оплаты\n"
        "• 📨 Изменить email - для чеков и уведомлений\n\n"
        "Все платежи безопасны и проходят через защищенные каналы.\n"
        "Чеки об оплате будут отправлены на указанный email."
    ),

    "payment_balance_button": "💰 Пополнить баланс",
    "payment_transactions_button": "💳 Мои транзакции",
    "payment_methods_button": "⚙️ Методы оплаты",
    "payment_change_email_button": "📨 Изменить email",


    "payment_choice_rub_button": "💳 Рубли",
    "payment_choice_crypt_button": "💲Криптовалюта",

    "payment_balance_pay_button": "💳 Оплатить",


    "back_to_main_menu_button": "⬅️ Назад",
    "payment_unknown_action": "Неизвестное действие.",
}

PROVIDER_BUTTON = {
    "YOOKASSA": "💳 ЮКасса: быстрая оплата",
    "YOOMONEY": "💳 ЮМани: перевод по карте",
    "FREEKASSA": "💰 FreeKassa: межд. платежи",
    "CRYPTOBOT": "💰 CryptoBot: криптовалюта",
    "STARS": "⭐ Оплата Звездами",
    "ROBOKASSA": "⭐ RoboKassa"
}