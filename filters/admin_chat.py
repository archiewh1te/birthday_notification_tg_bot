from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from data.config import load_config

config = load_config('.env')  # Load the configuration from .env file


class AdminFilter(BaseFilter):
    """ Filter that checks if a user is an admin. """

    async def __call__(
            self,
            obj: Union[Message, CallbackQuery],
    ) -> bool:

        user_id = obj.from_user.id  # Get the user ID

        if user_id in config.tg_bot.admin_id:
            return True
        else:
            await obj.answer('⛔️ Вы не Администратор! Данная команда не доступна ⛔️')
            return False
