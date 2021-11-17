from aiogram import Dispatcher

from filters.group_chat import IsGroups
from filters.not_banned import NotBanned
from loader import dp
# from .is_admin import AdminFilter


if __name__ == "filters":
    # dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(NotBanned)
    dp.filters_factory.bind(IsGroups)
