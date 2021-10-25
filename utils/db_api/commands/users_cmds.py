from loguru import logger

from utils.db_api.models import Users
from loguru import logger


# Добавление пользователя в бд
async def add_user(telegram_id: int, username: str = "Without a username") -> Users:
    try:
        return await Users(telegram_id=telegram_id, username=username).create()
    except Exception as ex:
        logger.info(ex)
