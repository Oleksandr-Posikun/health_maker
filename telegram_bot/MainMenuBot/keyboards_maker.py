from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardsMaker:
    async def create_inline_button(self, *buttons, row_width: int = 1):
        """
        This method creates one or more buttons for the inline keyboard.

        :param buttons: Example: {'text': 'btn_1', 'callback_data': 'btn_1'}
        :type buttons: dict
        :param row_width: Keyboard line width. Default is 1.
        :type row_width: int
        :return: InlineKeyboardMarkup object containing the built-in buttons.
        :rtype: InlineKeyboardMarkup
        """
        inline_keyboard = InlineKeyboardMarkup(row_width=row_width)
        for button in buttons:
            inline_keyboard.add(InlineKeyboardButton(text=button['text'], callback_data=button['callback_data']))

        return inline_keyboard

    async def create_reply_button(self, *args, row_width: int = 2, resize_keyboard: bool = True):
        buttons = [KeyboardButton(i) for i in args]
        keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=row_width).add(*buttons)

        return keyboard_menu
