from utils.db_api.commands.price_list_cmds import add_to_price_list


async def add_to_db_default_data():
    await add_to_price_list(name="🔥", price=100.00)
    await add_to_price_list(name="💰", price=75.00)
    await add_to_price_list(name="❤", price=50.00)
