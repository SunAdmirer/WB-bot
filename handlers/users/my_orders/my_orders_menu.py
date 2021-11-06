from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.my_orders.my_orders_menu_kb import my_orders_menu_kb
from utils.db_api.models import Users


async def my_orders_menu(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    text = "🛒 Мои заказы\n\n" \
           "Выберите категорию:"

    markup = await my_orders_menu_kb()

    await call.message.edit_text(text=text, reply_markup=markup)
