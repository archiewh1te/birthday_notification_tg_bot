import logging
import datetime
import os  # Импортируем модуль os
from logging.handlers import TimedRotatingFileHandler

format_msg = logging.Formatter(u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Путь к файлу лога
log_path = f'logs/server/logs_info {datetime.datetime.now().strftime("%Y-%m-%d")}.log'

# Проверяем, существует ли директория. Если нет, создаем ее.
if not os.path.exists(os.path.dirname(log_path)):
    os.makedirs(os.path.dirname(log_path))

file_handler = logging.handlers.TimedRotatingFileHandler(
    log_path,
    when='midnight',
    interval=1,
    encoding='utf-8')
file_handler.setFormatter(format_msg)

console_handler = logging.StreamHandler()
console_handler.setFormatter(format_msg)

logger.addHandler(file_handler)
logger.addHandler(console_handler)