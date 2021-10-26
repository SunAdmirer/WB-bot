from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from handlers.users.notifications import notifications
from keyboards.inline.callback_datas import main_menu_cd
from keyboards.inline.main_menu_kb import main_menu_kb
from loader import dp

from utils.db_api.models import Users


# Гавное меню
async def main_menu(message: [types.Message, types.CallbackQuery], **kwargs):
    # Клавиатура для сообщения
    markup = await main_menu_kb()

    # Сообщение главного меню
    if isinstance(message, types.Message):
        await message.answer("Main menu", reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text("Main menu", reply_markup=markup)


# Навигация в главном меню
@dp.callback_query_handler(NotBanned(), main_menu_cd.filter())
async def main_menu_nav(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')

    # Все функции
    functions = {
        'create_order': '',
        'list_orders': '',
        'referrals': '',
        'support': '',
        'balance': '',
        'my_orders': '',
        'notifications': notifications,
    }

    # Выбор функции в зависимости от нажатия кнопки
    function = functions.get(nav_btn)

    await function(
        call=call,
        user=user,
        state=state
    )
