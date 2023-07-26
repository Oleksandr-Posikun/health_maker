import asyncio

from __health_maker_bot.loader import bot, dp
from __health_maker_bot.main_bot import MainBot


main_bot = MainBot(bot, dp)


if __name__ == '__main__':
    asyncio.run(main_bot.app_run())
