from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from __health_maker_bot.config import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# client = config.CLIENT

memory = MemoryStorage()
dp = Dispatcher(bot, storage=memory)
