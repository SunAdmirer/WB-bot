from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


# Кастомный фильтр на групповой чат
class IsGroups(BoundFilter):
    async def check(self, message: [types.Message, types.CallbackQuery]):
        if isinstance(message, types.Message):
            return message.chat.type == types.ChatType.SUPERGROUP \
                   or message.chat.type == types.ChatType.GROUP

        elif isinstance(message, types.CallbackQuery):
            return message.message.chat.type == types.ChatType.SUPERGROUP \
                   or message.message.chat.type == types.ChatType.GROUP
