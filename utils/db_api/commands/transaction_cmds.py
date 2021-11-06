from utils.db_api.models import Transaction
from loguru import logger


async def add_translation(user_id: int, amount: float):
    try:
        await Transaction(user_id=user_id, amount=amount).create()
    except Exception as ex:
        logger.info(ex)
