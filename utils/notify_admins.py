import logging
import time

from aiogram import Bot

from data.config import load_config

config = load_config('.env')
# Уведомление администраторам бота о том что Бот запущен
date_now = time.strftime("%d-%m-%Y", time.localtime())
time_now = time.strftime("%H:%M:%S", time.localtime())


async def on_startup_notify(bot: Bot) -> None:
    """
    Notifies the bot administrators about the successful startup of the bot.

    Args:
        bot (Bot): The bot object.
    """
    for admin in config.tg_bot.dev_id:
        try:
            text = (f"✅Бот запущен и готов к работе!✅\n"
                    f"📅Дата: {date_now}\n"
                    f"⏰Время: {time_now}")
            await bot.send_message(chat_id=admin, text=text)
            print('Бот запущен')
        except Exception as err:
            logging.exception(err)
