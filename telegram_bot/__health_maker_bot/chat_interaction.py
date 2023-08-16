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
