import asyncio

from aiogram.utils import executor
from aiogram import types

from MainMenuBot.handler.view import MainMenu
from RunningWorkoutsBot.handler.view import RunningWorkouts
from WorkoutsMenuBot.handler.view import WorkoutMenu
from __health_maker_bot.config.config import ADMINS


class MainBot:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp
        self.main_menu = MainMenu(self.bot, self.dp)
        self.workout_menu = WorkoutMenu(self.bot, self.dp)
        self.running_workouts = RunningWorkouts(self.bot, self.dp)

    async def set_default_commands(self):
        await self.bot.set_my_commands([
            types.BotCommand('start', 'Запустити бота'),
            types.BotCommand('help', 'Покажу що я вмію!')
        ])

    async def start_polling(self):
        for admin in ADMINS:
            await self.bot.send_message(chat_id=admin, text='Бот запущен')

        await self.set_default_commands()

        self.main_menu.register_handlers()
        self.workout_menu.register_handlers()
        self.running_workouts.register_handlers()

    def app_run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.start_polling())
        executor.start_polling(self.dp, skip_updates=True)
