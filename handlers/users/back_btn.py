from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from handlers.users.main_menu import main_menu
from keyboards.inline.callback_datas import back_btn_cd
from loader import dp
from utils.db_api.models import Users


# Нажатия на книпки Назад и тд
@dp.callback_query_handler(NotBanned(), back_btn_cd.filter())
async def back_btn(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')

    function = ''

    # Вернуться в главное меню
    if nav_btn == 'main_menu':
        function = main_menu

    await function(
        message=call,
        call=call,
        user=user,
        state=state
    )
