from datetime import datetime
from aiogram import types

from MainMenuBot.FSM_obj import MainMenuState
from MainMenuBot.keyboards_maker import KeyboardsMaker
from RunningWorkoutsBot.FSM_obj import RunningState
from RunningWorkoutsBot.location_processing import LocationProcessing
from __health_maker_bot.https_request_security import httpsRequestSecurity
from __health_maker_bot.https_requests import HttpsRequestsServer


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
        self.time_list.append(datetime.now())
        time = await self.location_processing.get_interval_time()
        await self.bot.answer_callback_query(callback_query.id,
                                             text='Не забудьте вимкнути трансляцію!',
                                             show_alert=True)

        await self.bot.send_message(callback_query.message.chat.id,
                                    f"Вы прошли {round(sum(self.route_list), 2)} м "
                                    f"за {time['hours']:02d}:{time['minutes']:02d}:{time['seconds']:02d}")
        await self.location_processing.create_map()

        await MainMenuState.main_menu.set()

