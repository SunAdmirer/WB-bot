from utils.db_api.models import Users, Referrals
from loguru import logger


# Добавление рекрутера и рекрута
async def add_recruiter_and_recruit(recruiter: Users, recruit: Users):
    try:
        await Referrals(recruiter_id=recruiter.id, recruit_id=recruit.id).create()
    except Exception as ex:
        logger.info(ex)


# Узнаем кто привел пользователя
async def get_recruiter(recruit_id):
    try:
        return await Referrals.query.where(Referrals.recruit_id == recruit_id).gino.first()
    except Exception as ex:
        logger.info(ex)


# забирем бонус
async def change_bonus_false(_id: int):
    try:
        return await Referrals.update.values(bonus=False).where(Referrals.id == _id).gino.status()
    except Exception as ex:
        logger.info(ex)
