from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from handlers.users.create_order.favorites_order import favorites_order
from handlers.users.create_order.fire_order import fire_order
from handlers.users.create_order.redemption_order import redemption_order
from keyboards.inline.callback_datas import create_order_menu_cd
from keyboards.inline.create_order.create_order_menu_kb import create_order_menu_kb
from loader import dp
from utils.db_api.models import Users


# Меню создание заказа
async def create_order_menu(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    markup = await create_order_menu_kb()

    await call.message.edit_text("Выбери услугу",
                                 reply_markup=markup)


# Навигация в меню создание заказа
@dp.callback_query_handler(NotBanned(), create_order_menu_cd.filter())
async def create_order_menu_nav(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext,
                                **kwargs):
    nav_btn = callback_data.get('nav_btn')

    # Все функции
    functions = {
        '🔥': fire_order,
        '💰': redemption_order,
        '❤': favorites_order
    }

    # Выбор функции в зависимости от нажатия кнопки
    function = functions.get(nav_btn)

    await function(
        call=call,
        user=user,
        state=state
    )
