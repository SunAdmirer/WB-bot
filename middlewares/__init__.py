from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    pass
    # dp.middleware.setup(ThrottlingMiddleware())
