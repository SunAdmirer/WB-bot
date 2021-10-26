from gino import Gino
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRES_URI

db = Gino()


async def create_db():
    # устанавливаем связь с бд
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor

    # создание бд
    # await db.gino.drop_all()
    await db.gino.create_all()
