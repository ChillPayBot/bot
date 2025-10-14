MAIN_MENU = {
    "main_menu_greeting": "👋 Добро пожаловать в главное меню!\n\n🚀 Обходите блокировки, получайте доступ к любимому контенту и наслаждайтесь быстрой скоростью соединения.\n\n📖️ Выберите действие:",
    "menu_activate_trial_button": "🆓 Пробный период",
    "menu_subscribe_inline": "🌐 Купить VPN",
    "menu_my_profile_inline": "👤 Мой профиль",
    "menu_how_to_connect_button": "📖 Как подключить VPN",
    "menu_apply_promo_button": "🤝 Пригласить друзей",
    "menu_support_button": "🆘 Не работает VPN?",
    "main_menu_unknown_action": "Неизвестное действие.",

    "cancel_button": "❌ Отмена",
    "trial_confirm_activate_button": "✅ Активировать",
}

TARIFFS = {
    # ... (существующие тексты) ...
    "choose_tariff_message": "<b>Выберите подходящий тариф:</b>",
    "no_tariffs_available": "К сожалению, сейчас нет доступных тарифов. Попробуйте позже.",
    "error_loading_tariffs": "Произошла ошибка при загрузке тарифов. Пожалуйста, попробуйте еще раз.",
    "back_to_menu_button": "⬅️ Назад в меню",

    "tariff_description_quote": (
        "✨ <b>{name}</b> ({price}₽/мес)\n"
        "-------------------------------------\n"
        "🚀 <b>Скорость:</b> Без ограничений\n"
        "🌐 <b>Трафик:</b> {traffic_limit}\n"
        "💻 <b>Лимит устройств:</b> {devices_limit}\n\n"
        "⚡️ {benefit_line_1}\n"
        "💎 {benefit_line_2}"
    ),

    "tariff_select_button": "{name} — {price}₽/мес"
}


TRIAL = {
    "trial_confirmation_text": (
        "Вы собираетесь активировать бесплатный пробный период.\n\n"
        "⏳ <b>Срок действия:</b> 3 дня\n\n"
        "Вы получите полный доступ ко всем возможностям VPN. Продолжить?"
    ),
    "trial_success_message": (
        "✅ <b>Бесплатная подписка успешно активирована!</b>\n\n"
        "⏱️ <b>Срок действия:</b> {duration} дней\n\n"
        "📝 <b>Данные для подключения:</b>\n"
        "Ссылка для подключения:\n"
        "`{connection_link}`"  # Используем ` ` для моноширинного шрифта, чтобы ссылку было легко скопировать
    ),
    "trial_howto_connect_button": "📖 Как подключить VPN",
    "trial_back_to_menu_button": "⬅️ Вернуться в меню",
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