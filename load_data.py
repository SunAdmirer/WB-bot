import asyncio

from data import config
from utils.db_api import models
from utils.db_api.commands.orders_cmds import add_order, delete_order
from utils.db_api.commands.users_cmds import get_first_user


async def main():
    user = await get_first_user()
    for _ in range(1850):
        order = await add_order(user_id=user.id, type_order='❤')
        await delete_order(order.id)


loop = asyncio.get_event_loop()
loop.run_until_complete(models.db.set_bind(config.POSTGRES_URI))
loop.run_until_complete(main())
