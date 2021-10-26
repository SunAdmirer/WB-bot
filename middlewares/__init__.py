from aiogram import Dispatcher

from loader import dp
from .get_user import GetUser
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(GetUser())
    # dp.middleware.setup(ThrottlingMiddleware())
