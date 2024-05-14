import sqlite3

from data.config import load_config


async def create_table():
    config = load_config('.env')  # Load the configuration from .env file
    conn = sqlite3.connect(config.tg_bot.DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS birthdays (id INTEGER PRIMARY KEY AUTOINCREMENT, birthday DATE, first_name TEXT, last_name TEXT, edit_firstname TEXT, edit_lastname TEXT)")
    conn.commit()

    conn.close()
