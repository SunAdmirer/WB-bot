from typing import List

from utils.db_api.models import Users, Referrals
from loguru import logger


# Добавление пользователя в бд
async def add_user(telegram_id: int, username: str) -> Users:
    try:
        if username is None:
            username = "Without a username"

        return await Users(telegram_id=telegram_id, username=username).create()
    except Exception as ex:
        logger.info(ex)


# Получаем список всех пользователей
async def get_all_users() -> List[Users]:
    try:
        return await Users.query.gino.all()
    except Exception as ex:
        logger.info(ex)


async def get_first_user() -> Users:
    try:
        return await Users.query.gino.first()
    except Exception as ex:
        logger.info(ex)


# Получить кол-во рекрутов
async def count_recruit(recruiter_id) -> int:
    try:
        return len(await Referrals.query.where(Referrals.recruiter_id == recruiter_id).gino.all())
    except Exception as ex:
        logger.info(ex)


# Получить юзера за telegram id
async def get_user_by_telegram_id(telegram_id: int) -> Users:
    try:
        return await Users.query.where(Users.telegram_id == telegram_id).gino.first()
    except Exception as ex:
        logger.info(ex)


# Получить юзера за id
async def get_user_by_id(user_id: int) -> Users:
    try:
        return await Users.query.where(Users.id == user_id).gino.first()
    except Exception as ex:
        logger.info(ex)


# Вкл/Выкл уведомления
async def update_notification_user(telegram_id: int, notifications: bool):
    try:
        await Users.update.values(notifications=notifications).where(Users.telegram_id == telegram_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Увеличить баланс пользователя
async def increase_user_balance(user_id: int, amount: float):
    try:
        await Users.update.values(balance=Users.balance + amount).where(Users.id == user_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Увеличить баланс с реф. программы
async def increase_user_balance_from_ref(user_id: int, amount: float):
    try:
        await Users.update.values(balance_from_ref=Users.balance_from_ref + amount).where(Users.id == user_id).gino.status()
    except Exception as ex:
        logger.info(ex)


# Сколько заработал пользователь с реф. программы
async def get_balance_from_ref(user_id: int) -> float:
    try:
        user: Users = await Users.query.where(Users.id == user_id).gino.first()
        return user.balance_from_ref
    except Exception as ex:
        logger.info(ex)


# Уменьшить баланс пользователя
async def reduce_user_balance(user_id: int, amount: float):
    try:
        await Users.update.values(balance=Users.balance - amount).where(Users.id == user_id).gino.status()
    except Exception as ex:
        logger.info(ex)
