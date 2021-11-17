from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsGroups
from keyboards.inline.callback_datas import admins_confirmed_cd
from loader import dp

from utils.db_api.commands.orders_cmds import add_reserved_order_to_user, increase_by_1_orders_total_amount, \
    get_order_by_id, get_reserved_performers_order_by_id


# Подтверждение/Отклонение заявки на бронирование заказа
@dp.callback_query_handler(IsGroups(), admins_confirmed_cd.filter(confirm_type='app_confirm'), state="*")
async def admins_app_confirm_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')
    performer_id = int(callback_data.get('performer_id'))
    order_id = int(callback_data.get('order_id'))

    if nav_btn == "confirm":  # Подтверждение заявки на бронирование заказа
        # Достаем заказ
        order = await get_order_by_id(order_id)

        if order.goal_amount > order.total_amount:
            # Проверяем или исполнитель не бронировал заказ ранее
            check = await get_reserved_performers_order_by_id(user_id=performer_id, order_id=order_id)

            if not check:
                # Бронируем выполнение задания за пользователем
                await add_reserved_order_to_user(user_id=performer_id, order_id=order_id)

                # Увеличить total_amount заказа на 1
                await increase_by_1_orders_total_amount(order_id=order_id)

                # Уведомить пользователя
                # await func()

                await call.message.edit_text(f"✅ Подтверждение заявки на бронирование заказа({order_id}) одобрена!",
                                             reply_markup=None)
            else:
                await call.message.edit_text(f"❌ Исполнитерь уже выполняет заказ!",
                                             reply_markup=None)

        else:
            await call.message.edit_text(f"❌ На заказ({order_id}) набралось достаточно исполнителей!",
                                         reply_markup=None)

    elif nav_btn == 'reject':
        # Уведомить пользователя
        # await func()

        await call.message.edit_text(f"❌ Подтверждение заявки на бронирование заказа({order_id}) отклонена!",
                                     reply_markup=None)
