from aiogram import Router, types
from aiogram.filters import CommandStart
from keyboards.inline.user_keyboards import get_main_menu_keyboard

router = Router()

@router.message(CommandStart())
async def start_command_handler(message: types.Message):
    text = "Привет! 👋 Добро пожаловать в CHILLVPN!\nВыберите действие:"
    keyboard = get_main_menu_keyboard()
    await message.answer(text, reply_markup=keyboard)
