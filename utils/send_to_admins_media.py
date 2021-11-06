from aiogram import types

from data.config import ADMINS
from loader import bot


async def send_to_admins_media(media: types.MediaGroup):
    for admin in ADMINS:
        try:
            await bot.send_media_group(chat_id=admin, media=media)

        except Exception as err:
            pass
