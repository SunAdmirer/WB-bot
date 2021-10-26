from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.db_api.commands.users_cmds import get_user_by_telegram_id
from utils.db_api.models import Users


class GetUser(BaseMiddleware):

    @staticmethod
    async def on_process_message(message: types.Message, data: dict):
        await add_user_to_data(telegram_id=message.chat.id, data=data)

    @staticmethod
    async def on_process_inline_query(query: types.InlineQuery, data: dict):
        await add_user_to_data(telegram_id=query.from_user.id, data=data)

    @staticmethod
    async def on_process_callback_query(call: types.CallbackQuery, data: dict):
        # Убрать 'часики'
        await call.answer()
        await add_user_to_data(telegram_id=call.message.chat.id, data=data)


async def add_user_to_data(telegram_id: int, data: dict):
    user: Users = await get_user_by_telegram_id(telegram_id)
    data["user"] = user
