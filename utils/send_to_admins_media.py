from aiogram import types

from data.config import ADMINS_GROUP, ADMINS
from loader import bot


async def send_to_admins_media(media: types.MediaGroup):
    try:
        await bot.send_media_group(chat_id=ADMINS_GROUP, media=media)
    except Exception as err:
        pass
