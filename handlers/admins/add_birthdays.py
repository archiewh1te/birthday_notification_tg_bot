import sqlite3
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import load_config
from filters import PrivateChatFilter, AdminFilter
from state import state_add_birthday

config = load_config('.env')  # Load the configuration from .env file

router = Router(name='add_birthdays')


@router.message(F.text == "✏️ Добавить день рождения")
@router.message(Command('add_bd'), PrivateChatFilter(), AdminFilter())
async def cmd_add_birthday(message: Message, state: FSMContext):
    kb_cancel = InlineKeyboardMarkup(row_width=1,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text='❌ Отменить', callback_data='quit_add')
                                         ]
                                     ])
    msg_familiya = await message.reply('<b>Введите Фамилию (например: Иванов, Петров, Смирнов):</b> ',
                                       reply_markup=kb_cancel)
    await state.update_data(msg_1=msg_familiya)
    await state.set_state(state_add_birthday.familiya)


@router.message(state_add_birthday.familiya, PrivateChatFilter(), AdminFilter())
async def process_add_familiya(message: Message, state: FSMContext):
    your_familiya = message.text.strip()  # Убедитесь, что удалили начальные и конечные пробелы

    # Проверка на пустую строку или только пробелы
    if not your_familiya or your_familiya.isspace():
        await message.reply('❌ Фамилия не может быть пустой или состоять только из пробелов. Попробуйте еще раз')
        return

    # Проверка на наличие цифр
    if any(char.isdigit() for char in your_familiya):
        await message.reply('❌ Фамилия не может содержать цифры. Попробуйте еще раз')
        return

    # Приведение первой буквы к заглавной
    your_familiya = your_familiya.capitalize()
    await state.update_data(your_familiya=your_familiya)

    await state.set_state(state_add_birthday.familiya_plural)
    await message.reply(
        ' <b>Введите Фамилию в родительном падеже (у кого?) (например: Иванова, Петрова, Смирнова):</b>')


@router.message(state_add_birthday.familiya_plural, PrivateChatFilter(), AdminFilter())
async def process_add_familiya_plural(message: Message, state: FSMContext):
    your_plural_familiya = message.text.strip()  # Убедитесь, что удалили начальные и конечные пробелы

    # Проверка на пустую строку или только пробелы
    if not your_plural_familiya or your_plural_familiya.isspace():
        await message.reply('❌ Фамилия не может быть пустым или состоять только из пробелов. Попробуйте еще раз')
        return

    # Проверка на наличие цифр
    if any(char.isdigit() for char in your_plural_familiya):
        await message.reply('❌ Фамилия не может содержать цифры. Попробуйте еще раз')
        return

    # Приведение первой буквы к заглавной
    plural_familiya = your_plural_familiya.capitalize()
    await state.update_data(familiya_piural=plural_familiya)

    await state.set_state(state_add_birthday.name)
    await message.reply('<b>Введите Имя:</b> ')


@router.message(state_add_birthday.name, PrivateChatFilter(), AdminFilter())
async def process_add_name(message: Message, state: FSMContext):
    your_name = message.text.strip()  # Убедитесь, что удалили начальные и конечные пробелы

    # Проверка на пустую строку или только пробелы
    if not your_name or your_name.isspace():
        await message.reply('❌ Имя не может быть пустым или состоять только из пробелов. Попробуйте еще раз')
        return

    # Проверка на наличие цифр
    if any(char.isdigit() for char in your_name):
        await message.reply('❌ Имя не может содержать цифры. Попробуйте еще раз')
        return

    # Приведение первой буквы к заглавной
    your_name = your_name.capitalize()
    await state.update_data(your_name=your_name)

    await state.set_state(state_add_birthday.name_plural)
    await message.reply(' <b>Введите имя во множественном числе (например: Алексея, Андрея, Анны):</b>')


@router.message(state_add_birthday.name_plural, PrivateChatFilter(), AdminFilter())
async def process_add_name(message: Message, state: FSMContext):
    your_plural_name = message.text.strip()  # Убедитесь, что удалили начальные и конечные пробелы

    # Проверка на пустую строку или только пробелы
    if not your_plural_name or your_plural_name.isspace():
        await message.reply('❌ Имя не может быть пустым или состоять только из пробелов. Попробуйте еще раз')
        return

    # Проверка на наличие цифр
    if any(char.isdigit() for char in your_plural_name):
        await message.reply('❌ Имя не может содержать цифры. Попробуйте еще раз')
        return

    # Приведение первой буквы к заглавной
    plural_name = your_plural_name.capitalize()
    await state.update_data(name_piural=plural_name)

    await state.set_state(state_add_birthday.date)
    await message.reply('📆 <b>Введите дату рождения в формате гггг-мм-дд (например, 2000-01-01)</b>')


@router.message(state_add_birthday.date, PrivateChatFilter(), AdminFilter())
async def birthday_date(message: Message, state: FSMContext):
    try:
        birthday_date = datetime.strptime(message.text, '%Y-%m-%d').date()
        await state.update_data(date=birthday_date)
    except ValueError:
        await message.reply('❌ Неправильный формат даты. Попробуйте еще раз')
        return
    data = await state.get_data()
    your_familiya = data.get('your_familiya')
    your_familiya_plural = data.get('familiya_piural')
    your_name = data.get('your_name')
    your_plural = data.get('name_piural')
    your_date = data.get('date')
    msg_id = data.get('msg_1')

    conn = sqlite3.connect(config.tg_bot.DB_FILE)
    cursor = conn.cursor()

    # Добавление дату рождения в базу данных
    cursor.execute("INSERT INTO birthdays (birthday, first_name, last_name, edit_firstname, edit_lastname) VALUES (?, ?, ?, ?, ?)",
                   (your_date, your_familiya, your_name, your_familiya_plural, your_plural))
    conn.commit()

    conn.close()  # Закрыть соединение

    await state.clear()
    await msg_id.delete()
    await message.reply(f'✅ | <b>{your_familiya}</b> <b>{your_name}</b> | <b>{your_date}</b> | успешно добавлены!')


@router.callback_query(F.data.startswith('quit_add'), PrivateChatFilter(), AdminFilter())
async def quit_add(call: CallbackQuery, state: FSMContext) -> None:
    """
    Handles the 'quit' callback query, cancels the message sending process and informs the user.

    :param call: The CallbackQuery object representing the callback.
    :type call: aiogram.types.CallbackQuery
    :param state: The FSMContext object to manage bot states.
    :type state: aiogram.fsm.context.FSMContext
    """
    await state.clear()
    await call.message.delete()
    await call.message.answer('❌ <b>Действие отменено</b>')
