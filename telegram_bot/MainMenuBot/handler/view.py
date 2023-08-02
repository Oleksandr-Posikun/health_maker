from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo
from aiogram.utils.exceptions import MessageToDeleteNotFound

from MainMenuBot.FSM_obj import MainMenuState
from MainMenuBot.keyboards_maker import KeyboardsMaker
from RunningWorkoutsBot.FSM_obj import RunningState
from __health_maker_bot.https_requests import HttpsRequestsServer
from __health_maker_bot.https_request_security import httpsRequestSecurity


class MainMenu:
    def __init__(self, main_bot, main_dp):
        self.bot = main_bot
        self.dp = main_dp
        self.fsm_menu = MainMenuState()
        self.fsm_running = RunningState()
        self.keyboard = KeyboardsMaker()
        self.security_https = httpsRequestSecurity()
        self.server_request = HttpsRequestsServer()
        self.menu = [{
            'name': 'RunningWorkouts',
            'message': 'Вмикай геолокацию і починай бігти',
            'command': 'run',
            'fsm': self.fsm_running.start_run
        }]

    def register_handlers(self):
        self.dp.register_callback_query_handler(self.new_start, state=None)
        self.dp.register_message_handler(self.new_start, state=None)
        self.dp.register_message_handler(self.main_menu, commands=["menu"], state='*')
        self.dp.register_message_handler(self.help, lambda msg: msg.text.lower() == '/help',
                                         state=self.fsm_menu.get_class_variables() +
                                               self.fsm_running.get_class_variables())
        self.dp.register_callback_query_handler(self.choice_menu, lambda c: c.data, state=self.fsm_menu.main_menu)

    async def new_start(self, message: types.Message):
        telegram_id = str(message.from_user.id)
        user_name = str(message.from_user.username)
        user_first_name = str(message.from_user.first_name)
        token = self.security_https.generate_token(telegram_id, user_name)
        
        result = await self.server_request.post_user_info('check_user',
                                                          token,
                                                          telegram_id,
                                                          user_name)

        print(result)

        if result['data_state']['state'] == 'newbie':
            inline = await self.keyboard.create_inline_button({'text': 'Так', 'callback_data': 'yes'},
                                                              {'text': 'Ні', 'callback_data': 'no'},
                                                              row_width=2)

            await self.bot.send_message(message.from_user.id,
                                        f"Вітаю {user_first_name}. Бажаєш подивитися що я вмію?", reply_markup=inline)
        else:
            await self.bot.send_message(message.from_user.id,
                                        f"Вітаю {user_first_name}. "
                                        f"Було перезавантаження серверу, оберіть команду ще раз")
            await self.main_menu(message)

    async def main_menu(self, message: types.Message):
        main_menu = await self.keyboard.create_reply_button('help', 'start')

        inline_keyboard = await self.keyboard.create_inline_button(
            {'text': 'RunningWorkouts', 'callback_data': 'run'},
            row_width=2)

        await self.bot.send_message(message.from_user.id, "Головне меню", reply_markup=main_menu)
        await self.bot.send_message(message.from_user.id, "Обери тип заняття", reply_markup=inline_keyboard)

        await self.fsm_menu.main_menu.set()

    async def help(self, message: types.Message):
        await self.fsm_menu.main_menu.set()
        # markup = types.ReplyKeyboardMarkup()
        # markup.add(types.KeyboardButton('open',
        #                                 web_app=WebAppInfo(url='https://github.com/btholt/four-semesters-of-cs/blob'
        #                                                        '/fa61de3cc80e0030bb172ecd75c7cb4ca3aeeadf/index.html')))
        await self.bot.send_message(chat_id=message.from_user.id, text="Цей розділ поки ще в розробці")

    async def choice_menu(self, callback: types.CallbackQuery):
        for i in self.menu:
            if callback.data == i['command']:
                await self.bot.answer_callback_query(callback.id,
                                                     text=i['message'],
                                                     show_alert=True)

                await i['fsm'].set()

    async def clear_chat_memory(self, message):
        for i in range(message.message_id - message.message_id, message.message_id):
            try:
                await self.bot.delete_message(message.chat.id, message.message_id - i)
            except MessageToDeleteNotFound:
                break
