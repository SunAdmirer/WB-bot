from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.db_api.models import Users


# 🔥 Выкуп + отзыв + ❤
async def fire_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    text = "text fire_order"
