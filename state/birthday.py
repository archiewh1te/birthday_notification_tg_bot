from aiogram.fsm.state import StatesGroup, State


class state_add_birthday(StatesGroup):
    familiya = State()
    name = State()
    date = State()
    familiya_plural = State()
    name_plural = State()