from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.db_api.commands.orders_cmds import get_confirmed_paid_for_orders, get_performed_performers_orders
from utils.db_api.models import Users


async def list_orders_menu(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    # Получаем все задания, которые подтвердили и оплатили, но еще не выполненные
    orders = await get_confirmed_paid_for_orders()

    # Получаем выполненные задания исполнителя
    performed_orders = await get_performed_performers_orders(user_id=user.id)

    print(f"{orders=}")
    print(f"{performed_orders=}")
