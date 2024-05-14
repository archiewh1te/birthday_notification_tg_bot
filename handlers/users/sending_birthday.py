import asyncio
import sqlite3
import datetime

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message

from data.config import load_config
from filters import PrivateChatFilter

config = load_config('.env')  # Load the configuration from .env file

router = Router(name='sending_birthday')


# Функция для получения уведомлений о предстоящих днях рождения
async def check_upcoming_birthdays(bot: Bot):
    try:
        conn = sqlite3.connect(config.tg_bot.DB_FILE)
        cursor = conn.cursor()

        today = datetime.date.today()
        upcoming_birthdays_found = False

        cursor.execute(
            "SELECT birthday, edit_firstname, edit_lastname FROM birthdays WHERE strftime('%m-%d', birthday) BETWEEN strftime('%m-%d', date('now')) AND strftime('%m-%d', date('now', '+7 day'))",
        )
        upcoming_birthdays = cursor.fetchall()

        # Преобразуем полученные данные в словарь
        for row in upcoming_birthdays:
            date_str = row[0]
            familiya = row[1]
            name = row[2]

            date_birthday = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            current_date = datetime.datetime.now().date()
            days_left = (date_birthday.replace(
                year=current_date.year) - current_date).days  # Вычисляем разницу в днях

            upcoming_date = today + datetime.timedelta(days=days_left)

            if len(upcoming_birthdays) > 0:
                tomorrow = today + datetime.timedelta(days=1)  # Get tomorrow's date
                upcoming_birthdays_found = True
                if upcoming_date == datetime.date.today():  # Если сегодняшний день - день рождения
                    # Отправка поздравления
                    await bot.send_message(config.tg_bot.chat,
                                           f"🎉 С днем рождения, <b>{familiya}</b> <b>{name}</b>! 🥳🎊 Поздравляем тебя с этим особенным днем!")
                    await asyncio.sleep(10)
                    # Отправка уведомлений с отсчетом дней
                    if days_left > 0:  # Проверка, что осталось больше 0 дней до дня рождения
                        # Используем условные выражения для выбора правильной формы слова
                        if days_left == 1:
                            declension_days = "день"
                        elif 2 <= days_left % 10 <= 4:
                            declension_days = "дня"
                        else:
                            declension_days = "дней"
                        await bot.send_message(config.tg_bot.chat,
                                               f"🎁 Через {days_left} {declension_days} у <b>{familiya}</b> <b>{name}</b> день рождения!")
                    await asyncio.sleep(3)
                elif upcoming_date == tomorrow:  # If it's tomorrow's birthday
                    # Send the birthday message for tomorrow
                    await bot.send_message(config.tg_bot.chat,
                                           f"🎉 Завтра день рождения у <b>{familiya}</b> <b>{name}</b>! 🥳🎊 ")
                else:
                    # Используем условные выражения для выбора правильной формы слова
                    if days_left == 1:
                        declension_days = "день"
                    elif 2 <= days_left % 10 <= 4:
                        declension_days = "дня"
                    else:
                        declension_days = "дней"
                    # Отправка уведомлений с отсчетом дней
                    await bot.send_message(config.tg_bot.chat,
                                           f"🎁 Через {days_left} {declension_days} у <b>{familiya}</b> <b>{name}</b> день рождения!")
                    if upcoming_date == tomorrow:  # If it's tomorrow's birthday
                        await bot.send_message(config.tg_bot.chat,
                                               f"🎉 Завтра день рождения у <b>{familiya}</b> <b>{name}</b>! 🥳🎊 ")
        if not upcoming_birthdays_found:  # Если не найдены ближайшие дни рождения
            await bot.send_message(config.tg_bot.chat, "☹️ В ближайшие дни ни у кого нет дня рождения.")
        conn.close()
    except Exception as e:
        print(e)


# Функция для получения у кого сегодня день рождение по команде /bd_check
@router.message(F.text == "🎁 Просмотреть дни рождения")
@router.message(Command('bd_check'), PrivateChatFilter())
async def check_today_birthdays(message: Message):
    try:
        conn = sqlite3.connect(config.tg_bot.DB_FILE)
        cursor = conn.cursor()

        today = datetime.date.today()
        upcoming_birthdays_found = False

        cursor.execute(
            "SELECT birthday, edit_firstname, edit_lastname FROM birthdays WHERE strftime('%m-%d', birthday) BETWEEN strftime('%m-%d', date('now')) AND strftime('%m-%d', date('now', '+7 day'))",
        )
        upcoming_birthdays = cursor.fetchall()

        # Преобразуем полученные данные в словарь
        for row in upcoming_birthdays:
            date_str = row[0]
            familiya = row[1]
            name = row[2]

            date_birthday = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            current_date = datetime.datetime.now().date()
            days_left = (date_birthday.replace(
                year=current_date.year) - current_date).days  # Вычисляем разницу в днях

            upcoming_date = today + datetime.timedelta(days=days_left)

            if len(upcoming_birthdays) > 0:
                tomorrow = today + datetime.timedelta(days=1)  # Get tomorrow's date
                upcoming_birthdays_found = True
                if upcoming_date == datetime.date.today():  # Если сегодняшний день - день рождения
                    # Отправка поздравления
                    await message.answer(
                        f"🎉 Сегодня день рождения у <b>{familiya}</b> <b>{name}</b>! 🥳🎊 ")
                    await asyncio.sleep(10)
                    # Отправка уведомлений с отсчетом дней
                    if days_left > 0:  # Проверка, что осталось больше 0 дней до дня рождения
                        # Используем условные выражения для выбора правильной формы слова
                        if days_left == 1:
                            declension_days = "день"
                        elif 2 <= days_left % 10 <= 4:
                            declension_days = "дня"
                        else:
                            declension_days = "дней"
                        await message.answer(f"🎁 Через {days_left} {declension_days} у <b>{familiya}</b> <b>{name}</b> день рождения!")
                    await asyncio.sleep(3)
                elif upcoming_date == tomorrow:  # If it's tomorrow's birthday
                    # Send the birthday message for tomorrow
                    await message.answer(f"🎉 Завтра день рождения у <b>{familiya}</b> <b>{name}</b>! 🥳🎊 ")
                else:
                    # Используем условные выражения для выбора правильной формы слова
                    if days_left == 1:
                        declension_days = "день"
                    elif 2 <= days_left % 10 <= 4:
                        declension_days = "дня"
                    else:
                        declension_days = "дней"
                    # Отправка уведомлений с отсчетом дней
                    await message.answer(f"🎁 Через {days_left} {declension_days} у <b>{familiya}</b> <b>{name}</b> день рождения!")
                    if upcoming_date == tomorrow:  # If it's tomorrow's birthday
                        await message.answer(f"🎉 Завтра день рождения у <b>{familiya}</b> <b>{name}</b>! 🥳🎊 ")
        if not upcoming_birthdays_found:  # Если не найдены ближайшие дни рождения
            await message.answer("☹️ В ближайшие дни ни у кого нет дня рождения.")
        conn.close()
    except Exception as e:
        print(e)
