import asyncio
import datetime

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import DeleteWebhook

from data.config import load_config
from database.models.base import create_table
from handlers.users import start, sending_birthday
from handlers.admins import add_birthdays
from handlers.users.sending_birthday import check_upcoming_birthdays
from middlewares import ThrottlingMiddleware
from utils.commands import set_default_commands
from utils.notify_admins import on_startup_notify
import utils.logging


async def main():
    config = load_config('.env')  # Load the configuration from .env file
    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(ThrottlingMiddleware())  # Registration of middleware

    await set_default_commands(bot)
    await on_startup_notify(bot)
    await create_table()

    try:
        # Connection of handlers to the bot
        dp.include_routers(
            start.router,
            add_birthdays.router,
            sending_birthday.router,

        )
        await bot(DeleteWebhook(drop_pending_updates=True))
        daily_check_task = asyncio.create_task(daily_check(bot))  # Запуск функции daily_check
        await dp.start_polling(bot)
        await daily_check_task  # Ожидание завершения функции daily_check

    finally:
        await bot.session.close()


async def daily_check(bot):
    while True:
        now = datetime.datetime.now()
        target_time = datetime.datetime(now.year, now.month, now.day, 9, 5)

        if now > target_time:
            target_time += datetime.timedelta(days=1)

        wait_time = (target_time - now).total_seconds()
        await asyncio.sleep(wait_time)
        await check_upcoming_birthdays(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
