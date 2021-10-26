from utils.db_api.models import Users
from loguru import logger


# Добавление пользователя в бд
async def add_user(telegram_id: int, username: str) -> Users:
    try:
        if username is None:
            username = "Without a username"

        return await Users(telegram_id=telegram_id, username=username).create()
    except Exception as ex:
        logger.info(ex)


# Получить юзера за telegram id
async def get_user_by_telegram_id(telegram_id: int) -> Users:
    try:
        return await Users.query.where(Users.telegram_id == telegram_id).gino.first()
    except Exception as ex:
        logger.info(ex)


# Вкл/Выкл уведомления
async def update_notification_user(telegram_id: int, notifications: bool):
    try:
        await Users.update.values(notifications=notifications).where(Users.telegram_id == telegram_id).gino.status()
    except Exception as ex:
        logger.info(ex)
