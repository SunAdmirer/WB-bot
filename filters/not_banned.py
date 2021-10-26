from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils.db_api.commands.users_cmds import get_user_by_telegram_id
from utils.db_api.models import Users


class NotBanned(BoundFilter):
    async def check(self, update: [types.Message, types.CallbackQuery]) -> bool:

        if isinstance(update, types.Message):
            telegram_id = update.chat.id
        elif isinstance(update, types.CallbackQuery):
            telegram_id = update.message.chat.id
        else:
            return True  # Пользователь не забанен

        # Получаем пользователя
        user: Users = await get_user_by_telegram_id(telegram_id)

        if user:
            if user.restricted:
                return False  # Пользователь забанен
            else:
                return True  # Пользователь не забанен
        else:
            return True  # Пользователь не забанен
