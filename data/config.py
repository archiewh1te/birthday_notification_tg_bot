from dataclasses import dataclass

from environs import Env


@dataclass
class TelegramBot:
    token: str  # Telegram bot token
    admin_id: list[int]  # List of bot admins
    dev_id: list[int]
    DB_FILE: str
    chat: str


@dataclass
class Miscellaneous:
    other_params: str = None  # Your other params


@dataclass
class Config:
    tg_bot: TelegramBot
    misc: Miscellaneous


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)  # If the path is not specified, it is equal to .env

    return Config(
        tg_bot=TelegramBot(
            token=env.str("BOT_TOKEN"),
            admin_id=list(map(int, env.list("ADMINS"))),
            dev_id=list(map(int, env.list("DEV_ID"))),
            DB_FILE=env.str("DB_FILE"),
            chat=env.str("CHAT"),

        ),
        misc=Miscellaneous()
    )
