from utils.db_api.models import PriceList
from loguru import logger


async def add_to_price_list(name: str, price: float):
    try:
        await PriceList(name=name, price=price).create()
    except Exception as ex:
        pass


async def get_price_by_name(name: str) -> PriceList:
    try:
        return await PriceList.query.where(PriceList.name == name).gino.first()
    except Exception as ex:
        logger.info(ex)
