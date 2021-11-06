from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.referrals_kb import referrals_kb
from utils.db_api.models import Users


async def referrals(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    text = "пригласить друга"

    markup = await referrals_kb()

    await call.message.edit_text(text=text, reply_markup=markup)
