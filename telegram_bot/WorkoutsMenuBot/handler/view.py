from aiogram import types

from MainMenuBot.FSM_obj import MainMenuState
from MainMenuBot.keyboards_maker import KeyboardsMaker
from RunningWorkoutsBot.FSM_obj import RunningState
from RunningWorkoutsBot.interface import MenuInterface
from WorkoutsMenuBot.FSM_obj import WorkoutsMenuState


class WorkoutMenu(MenuInterface):
    def __init__(self, main_bot, main_dp):
        self.bot = main_bot
        self.dp = main_dp
        self.fsm_main_menu = MainMenuState()
        self.fsm_workouts_menu = WorkoutsMenuState()
        self.fsm_running = RunningState()
        self.keyboard = KeyboardsMaker()

        self.menu_list = [{
            'name': 'RunningWorkouts',
            'message': 'Вмикай геолокацию і починай бігти',
            'command': 'run',
            'fsm': self.fsm_running.start_run
        }]

    def register_handlers(self):
        self.dp.register_callback_query_handler(self.menu, state=self.fsm_main_menu.workout_menu)
        self.dp.register_callback_query_handler(self.choice_done, lambda c: c.data,
                                                state=self.fsm_workouts_menu.run_workout)

    async def menu(self, callback: types.CallbackQuery):
        main_menu = await self.keyboard.create_reply_button('🆘 help')

        inline_keyboard = await self.keyboard.create_inline_button(
            {'text': 'RunningWorkouts', 'callback_data': 'run'},
            row_width=2)

        await self.bot.send_message(callback.message.chat.id, "Тренування", reply_markup=main_menu)
        await self.bot.send_message(callback.message.chat.id, "Обери тип заняття____", reply_markup=inline_keyboard)

        await self.fsm_workouts_menu.run_workout.set()

    async def choice_done(self, callback: types.CallbackQuery):
        await self.choice(callback, self.menu_list)

    async def choice(self, callback: types.CallbackQuery, menu_list):
        for i in menu_list:
            if callback.data == i['command']:
                await self.bot.answer_callback_query(callback.id,
                                                     text=i['message'],
                                                     show_alert=True)

                await i['fsm'].set()
