import logging
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, FSInputFile, InputMediaPhoto, BufferedInputFile
from aiogram.exceptions import TelegramBadRequest
from typing import Union, Optional
from pathlib import Path
import os
import aiofiles
import asyncio

logger = logging.getLogger(__name__)


async def edit_or_send_message(
        target_event: Union[Message, CallbackQuery],
        text: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        media_path: Optional[Path] = None,  # 💥 Теперь принимаем Path
        parse_mode: str = 'HTML'
):
    # Извлекаем message и chat_id для удобства
    target_message = target_event.message if isinstance(target_event, CallbackQuery) else target_event
    chat_id = target_event.from_user.id

    # Отвечаем на колбэк, чтобы убрать часы
    if isinstance(target_event, CallbackQuery):
        await target_event.answer()

    # --- 1. ЛОГИКА С МЕДИА (Отправка или Редактирование медиа) ---

    # 💥 ИСПОЛЬЗУЕМ ВАШ КОД: Если предоставлен путь к новому медиа
    if media_path and os.path.isfile(media_path):

        # 1.1. Асинхронно считываем данные файла
        async with aiofiles.open(media_path, "rb") as f:
            image_data = await f.read()

        # 1.2. Создаем BufferedInputFile для отправки
        buffered_file = BufferedInputFile(image_data, filename=os.path.basename(media_path))

        # 1.3. Пробуем отредактировать медиа, если это CallbackQuery
        if isinstance(target_event, CallbackQuery):
            media = InputMediaPhoto(
                media=buffered_file,
                caption=text,
                parse_mode=parse_mode
            )
            try:
                await target_message.edit_media(media=media, reply_markup=reply_markup)
                return
            except Exception as e:
                logger.warning(f"Не удалось отредактировать медиа, отправляем новое сообщение. Ошибка: {e}")

        # 1.4. Отправляем новое фото (если это /start или edit_media не удался)
        await target_event.bot.send_photo(
            chat_id=chat_id,
            photo=buffered_file,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )
        # Если это был /start, мы ответили. Если CallbackQuery, мы отправили новое сообщение.
        # В случае CallbackQuery, старое сообщение часто остается, если не удалить.
        # Однако, при переходе с /start на /start это лучший вариант.
        return

    # --- 2. ЛОГИКА БЕЗ НОВОГО МЕДИА (Редактирование текста/подписи или Отправка) ---

    # 2.1. Попробуем отредактировать подпись, если это фото-сообщение
    if target_message.caption is not None and isinstance(target_event, CallbackQuery):
        try:
            await target_message.edit_caption(
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            return
        except TelegramBadRequest as e:
            # Ошибка, что текст не изменился, игнорируем
            if "message is not modified" in str(e):
                return
            logger.warning(f"Ошибка edit_caption (пробуем edit_text): {e}")

    # 2.2. Попробуем отредактировать текст
    if isinstance(target_event, CallbackQuery):
        try:
            await target_message.edit_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            return
        except TelegramBadRequest as e:
            if "message is not modified" in str(e):
                return
            logger.warning(f"Ошибка edit_text (пробуем отправить новое): {e}")
        except Exception as e:
            logger.warning(f"Непредвиденная ошибка edit_text: {e}")

    # 2.3. Если все редактирования не удались или это Message (ответ на /start без фото)
    await target_message.answer(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )
