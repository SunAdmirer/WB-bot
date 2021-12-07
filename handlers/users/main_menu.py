from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from handlers.users.balance.balance_menu import balance_menu
from handlers.users.create_order.create_order_menu import create_order_menu
from handlers.users.list_orders.list_orders_menu import list_orders_menu
from handlers.users.my_orders.my_orders_menu import my_orders_menu
from handlers.users.notifications import notifications
from handlers.users.referrals import referrals
from keyboards.inline.callback_datas import main_menu_cd
from keyboards.inline.main_menu_kb import main_menu_kb
from loader import dp

from utils.db_api.models import Users


# Гавное меню
async def main_menu(message: [types.Message, types.CallbackQuery], **kwargs):
    # Клавиатура для сообщения
    markup = await main_menu_kb()

    text = "👋 Привет.\n" \
           "Круто, что ты теперь с нами\n\n" \
           "Мы считаем польза есть во всем. Особенно в боте" \
           " с БЕСПЛАТНЫМИ товарами. С ним ты получишь товар" \
           " бесплатно и вернешь свое за покупки."

    # Сообщение главного меню
    if isinstance(message, types.Message):
        await message.answer(text, reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(text, reply_markup=markup)


# Навигация в главном меню
@dp.callback_query_handler(NotBanned(), main_menu_cd.filter())
async def main_menu_nav(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')

    # Все функции
    functions = {
        'create_order': create_order_menu,
        'list_orders': list_orders_menu,
        'referrals': referrals,
        'support': '',
        'balance': balance_menu,
        'my_orders': my_orders_menu,
        'notifications': notifications,
    }

    # Выбор функции в зависимости от нажатия кнопки
    function = functions.get(nav_btn)

    await function(
        call=call,
        user=user,
        state=state
    )
