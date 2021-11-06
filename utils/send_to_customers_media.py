from aiogram import types

from loader import bot
from utils.db_api.models import Users


async def send_to_customers_media(media: types.MediaGroup, customer: Users):
    try:
        await bot.send_media_group(chat_id=customer.telegram_id, media=media)

    except Exception as err:
        pass
