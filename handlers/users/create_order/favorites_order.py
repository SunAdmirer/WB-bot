from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.db_api.models import Users


async def favorites_order(call: types.CallbackQuery, user: Users, state: FSMContext):
    pass
