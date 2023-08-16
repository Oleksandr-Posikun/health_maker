from aiogram.utils.exceptions import MessageToDeleteNotFound


class ChatInteraction:
    def __init__(self, main_bot, main_dp):
        self.bot = main_bot
        self.dp = main_dp

    async def clear_chat_memory(self, message):
        for i in range(message.message_id - message.message_id, message.message_id):
            try:
                await self.bot.delete_message(message.chat.id, message.message_id - i)
            except MessageToDeleteNotFound:
                break

    async def callback_clear_chat_memory(self, callback):
        for i in range(callback.message.message_id - callback.message.message_id, callback.message.message_id):
            try:
                await self.bot.delete_message(callback.message.chat.id, callback.message.message_id - i)
            except MessageToDeleteNotFound:
                break

    async def callback_delete_message_index(self, callback, index):
        await self.bot.delete_message(callback.message.chat.id, callback.message.message_id-index)

    async def delete_message_index(self, message, index):
        await self.bot.delete_message(message.chat.id, message.message_id-index)
