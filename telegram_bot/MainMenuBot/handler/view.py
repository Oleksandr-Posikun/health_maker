from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo

from MainMenuBot.FSM_obj import MainMenuState
from MainMenuBot.keyboards_maker import KeyboardsMaker
from RunningWorkoutsBot.FSM_obj import RunningState
from RunningWorkoutsBot.interface import MenuInterface
from WorkoutsMenuBot.handler.view import WorkoutMenu
from __health_maker_bot.chat_interaction import ChatInteraction
from __health_maker_bot.https_requests import HttpsRequestsServer
from __health_maker_bot.https_request_security import httpsRequestSecurity


class MainMenu(MenuInterface):
    def __init__(self, main_bot, main_dp):
        self.bot = main_bot
        self.dp = main_dp
        self.fsm_main_menu = MainMenuState()
        self.fsm_running = RunningState()
        self.chat_interaction = ChatInteraction(main_bot, main_dp)
        self.keyboard = KeyboardsMaker()
        self.security_https = httpsRequestSecurity()
        self.server_request = HttpsRequestsServer()
        self.workout_menu = WorkoutMenu(main_bot, main_dp)
        self.menu_list = [{
            'name': 'WorkoutsMenu',
            'message': 'меню спорту',
            'command': 'workouts',
            'fsm': self.fsm_main_menu.workout_menu
        },
            {
                'name': 'FoodMenu',
                'message': 'меню їжи',
                'command': 'food',
                'fsm': self.fsm_main_menu.food_menu
            }
        ]

    def register_handlers(self):
        self.dp.register_callback_query_handler(self.new_start, state=None)
        self.dp.register_message_handler(self.new_start, state=None)
        self.dp.register_callback_query_handler(self.menu, text=["menu"], state='*')
        self.dp.register_message_handler(self.help, lambda msg: msg.text.lower() == '🆘 help',
                                         state=self.fsm_main_menu.get_class_variables() +
                                               self.fsm_running.get_class_variables())
        self.dp.register_callback_query_handler(self.choice_done, lambda c: c.data, state=self.fsm_main_menu.main_menu)

    async def new_start(self, message: types.Message):
        telegram_id = str(message.from_user.id)
        user_name = str(message.from_user.username)
        user_first_name = str(message.from_user.first_name)
        token = self.security_https.generate_token(telegram_id, user_name)
        
        result = await self.server_request.post_user_info('check_user',
                                                          token,
                                                          telegram_id,
                                                          user_name)

        if result['data_state']['state'] == 'newbie':
            inline = await self.keyboard.create_inline_button({'text': 'Так', 'callback_data': 'yes'},
                                                              {'text': 'Ні', 'callback_data': 'no'},
                                                              row_width=2)

            await self.bot.send_message(message.chat.id,
                                        f"Вітаю {user_first_name}. Бажаєш подивитися що я вмію?",
                                        reply_markup=inline)
        else:
            if isinstance(message, types.CallbackQuery):
                await self.bot.send_message(message.message.chat.id,
                                            f"Вітаю {user_first_name}. "
                                            f"Було перезавантаження серверу, оберіть команду ще раз")
            elif isinstance(message, types.Message):
                await self.bot.send_message(message.chat.id,
                                            f"Вітаю {user_first_name}. "
                                            f"Було перезавантаження серверу, оберіть команду ще раз")

            await self.menu(message)

    async def help(self, message: types.Message):
        await self.fsm_main_menu.main_menu.set()
        # markup = types.ReplyKeyboardMarkup()
        # markup.add(types.KeyboardButton('open',
        #                                 web_app=WebAppInfo(url='')))
        await self.bot.send_message(chat_id=message.from_user.id, text="Цей розділ поки ще в розробці")

    async def menu(self, message):
        inline_keyboard = await self.keyboard.create_inline_button(
            {'text': 'Тренування', 'callback_data': 'workouts'},
            {'text': 'Харчування', 'callback_data': 'food'},
            row_width=2)

        if isinstance(message, types.CallbackQuery):
            await self.bot.send_message(message.message.chat.id, "Оберіть меню:",
                                        reply_markup=inline_keyboard)

        if isinstance(message, types.Message):
            await self.bot.send_message(message.chat.id, "Оберіть меню:", reply_markup=inline_keyboard)

        await self.fsm_main_menu.main_menu.set()

    async def choice(self, callback: types.CallbackQuery, menu_list):
        inline = await self.keyboard.create_inline_button({'text': 'Так', 'callback_data': 'yes'},
                                                          {'text': 'Ні', 'callback_data': 'no'},
                                                          row_width=2)
        for i in menu_list:
            if callback.data == i['command']:
                await self.bot.edit_message_text(chat_id=callback.message.chat.id,
                                                 message_id=callback.message.message_id,
                                                 text=i['message'],
                                                 reply_markup=inline)

                await i['fsm'].set()

    async def choice_done(self, callback: types.CallbackQuery):
        await self.choice(callback, self.menu_list)
