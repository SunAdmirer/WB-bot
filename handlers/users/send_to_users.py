from loguru import logger

from keyboards.inline.send_to_users_kb import send_to_users_kb
from loader import bot
from utils.db_api.commands.users_cmds import get_all_users


# Отправка сообщения всем пользователям
async def send_to_users(text: str):
    users = await get_all_users()

    markup = await send_to_users_kb()

    for user in users:
        if user.notifications:
            try:
                await bot.send_message(chat_id=user, text=text, reply_markup=markup)
            except Exception as ex:
                logger.info(ex)
