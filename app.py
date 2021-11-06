from aiogram import executor

from loader import dp, bot, start_scheduler
import middlewares, filters, handlers
from utils.db_api.add_to_db_default_data import add_to_db_default_data
from utils.db_api.database import create_db
from utils.misc.logger import setup_logger
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):

    # Соединение с бд
    await create_db()

    # Добавление default data в базу. (Цены на услуги и тд)
    await add_to_db_default_data()

    # запуск scheduler
    start_scheduler()

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    # await on_startup_notify(dispatcher)


async def on_shutdown(dp):
    print("Can we stop it?")
    dp.stop_polling()
    await dp.wait_closed()
    await bot.close()
    print("Yes, we can!")


if __name__ == '__main__':
    setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    executor.start_polling(dp, on_startup=on_startup)

