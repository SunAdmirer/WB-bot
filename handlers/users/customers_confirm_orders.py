from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from keyboards.inline.callback_datas import customers_confirmed_cd
from keyboards.inline.customers_performed_orders_kb import customers_confirmed_order_kb
from keyboards.inline.send_to_users_kb import send_to_users_kb
from loader import dp, bot
from loguru import logger

# Подтверждение
from utils.db_api.commands.orders_cmds import update_moderate_order_confirmed, get_order_by_id
from utils.db_api.commands.users_cmds import get_user_by_id


@dp.callback_query_handler(NotBanned(), customers_confirmed_cd.filter(confirm_type="confirmed"), state="*")
async def customers_confirmed_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    performer_id = int(callback_data.get('performer_id'))
    customer_id = int(callback_data.get('customer_id'))
    order_id = int(callback_data.get('order_id'))

    markup = await customers_confirmed_order_kb(order_id=order_id, customer_id=customer_id)
    await call.message.edit_text("✅ Вы уверены, что подтверждаете заказ?",
                                 reply_markup=markup)


# Отклонение
@dp.callback_query_handler(NotBanned(), customers_confirmed_cd.filter(confirm_type="reject"), state="*")
async def customers_reject_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    pass


@dp.callback_query_handler(NotBanned(), customers_confirmed_cd.filter(confirm_type="confirmed2"), state="*")
async def double_customers_confirmed_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    performer_id = int(callback_data.get('performer_id'))
    customer_id = int(callback_data.get('customer_id'))
    order_id = int(callback_data.get('order_id'))

    performer = await get_user_by_id(performer_id)
    customer = await get_user_by_id(customer_id)

    # Подтверждаем выполнение
    await update_moderate_order_confirmed(order_id=order_id, confirmed=True)

    # Достаем заказ
    order = await get_order_by_id(order_id)

    markup = await send_to_users_kb()

    await call.message.edit_text("✅ Отлично! Исполнитель получил подтверждение заказа.")

    try:
        await bot.send_message(chat_id=performer.telegram_id,
                               text=f"✅ Выполнение заказа {order.order_name} подтверждено!",
                               reply_markup=markup)
    except Exception as ex:
        logger.info(ex)
