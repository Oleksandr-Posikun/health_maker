from aiogram import types


class MenuInterface:
    def register_handlers(self):
        pass

    def menu(self, callback):
        pass

    def choice(self, callback: types.CallbackQuery, menu_list: list):
        pass

    def choice_done(self, callback: types.CallbackQuery):
        pass
