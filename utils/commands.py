from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


# Команды в меню бота
async def set_default_commands(bot: Bot) -> None:
    """
    Sets the default commands for the bot.

    Args:
        bot (Bot): The bot object.
    """
    commands = ([
        BotCommand(command='start', description='Запустить бота'),
        BotCommand(command='bd_check', description='Дни рождения'),
    ])

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
