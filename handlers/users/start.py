from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message

from data.config import load_config
from filters import PrivateChatFilter

config = load_config('.env')  # Load the configuration from .env file

router = Router(name='start')


# Команды бота
@router.message(CommandStart(), PrivateChatFilter())
async def cmd_start(message: Message):
    kb = [
        [types.KeyboardButton(text="✏️ Добавить день рождения")],
        [types.KeyboardButton(text="🎁 Просмотреть дни рождения")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(
        f'✋ Привет <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a></b>! \n'
        f'🎁 Я бот уведомлений о днях рождения. Чтобы посмотреть у кого сегодня день рождение используй клавиатуру '
        f'или команду /bd_check', reply_markup=keyboard)



