from datetime import datetime
from aiogram import types

from MainMenuBot.FSM_obj import MainMenuState
from MainMenuBot.keyboards_maker import KeyboardsMaker
from RunningWorkoutsBot.FSM_obj import RunningState
from RunningWorkoutsBot.location_processing import LocationProcessing


class RunningWorkouts:
    def __init__(self, main_bot, main_dp):
        self.bot = main_bot
        self.dp = main_dp
        self.fsm_running = RunningState()
        self.keyboard = KeyboardsMaker()
        self.location_processing = LocationProcessing()

    def register_handlers(self):
        self.dp.register_message_handler(self.start_handle_location,
                                         content_types=types.ContentType.LOCATION,
                                         state=self.fsm_running.start_run)
        self.dp.register_edited_message_handler(self.moving_handle_location,
                                                content_types=types.ContentType.LOCATION,
                                                state=self.fsm_running.moving)
        self.dp.register_callback_query_handler(self.finish_handle_location, text=['finish'],
                                                state=self.fsm_running.moving)

    async def start_handle_location(self, message: types.Message):
        await self.location_processing.request_coordinates(message, 'start_running_workouts')

        inline_keyboard = await self.keyboard.create_inline_button({'text': 'Фініш', 'callback_data': 'finish'})

        await message.answer('Натисни "Фініш" коли закінчиш пробіжку:', reply_markup=inline_keyboard)

        await self.fsm_running.moving.set()

    async def moving_handle_location(self, message: types.Message):
        await self.location_processing.request_coordinates(message, 'running_workouts_lasts')

    async def finish_handle_location(self, callback_query: types.CallbackQuery):
        result = await self.location_processing.requests_finish_location(callback_query, 'running_workouts_finish')
        time_seconds = float(result['time'])

        hours = int(time_seconds // 3600)
        minutes = int((time_seconds % 3600) // 60)
        seconds = int(time_seconds % 60)
        milliseconds = int((time_seconds % 1) * 1000)

        await self.bot.send_message(callback_query.message.chat.id,
                                    f"Відстань : {round(result['distance'], 2)} м \n"
                                    f"Час {hours:02}:{minutes:02}:{seconds:02}:{milliseconds:03} \n"
                                    f"Ваша швидкість {round(result['speed']['speed'], 2)} м/с ->"
                                    f"{round(result['speed']['converted speed'], 2)} км/г")

        await MainMenuState.main_menu.set()
