from utils.db_api.models import Users, Referrals
from loguru import logger


# Добавление рекрутера и рекрута
async def add_recruiter_and_recruit(recruiter: Users, recruit: Users):
    try:
        await Referrals(recruiter_id=recruiter.id, recruit_id=recruit.id).create()
    except Exception as ex:
        logger.info(ex)
