from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from keyboards.inline.callback_datas import customers_confirmed_cd
from keyboards.inline.customers_performed_orders_kb import customers_confirmed_order_kb
from keyboards.inline.send_to_users_kb import send_to_users_kb
from loader import dp, bot
from loguru import logger
from utils.db_api.commands.orders_cmds import update_moderate_order_confirmed, get_order_by_id, delete_moderate_order, \
    delete_reserved_order_to_user, add_performed_order
from utils.db_api.commands.users_cmds import get_user_by_id, increase_user_balance

# Подтверждение
from utils.send_to_customers_performed_order import send_to_customers_performed_order


@dp.callback_query_handler(NotBanned(), customers_confirmed_cd.filter(confirm_type="customer_performed"), state="*")
async def customers_confirmed_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')
    performer_id = int(callback_data.get('performer_id'))
    customer_id = int(callback_data.get('customer_id'))
    order_id = int(callback_data.get('order_id'))

    performer = await get_user_by_id(performer_id)

    # Достаем заказ
    order = await get_order_by_id(order_id)

    if nav_btn == 'confirm':
        markup = await customers_confirmed_order_kb(performer_id=performer.id,
                                                    confirm_type='customer_confirm2',
                                                    customer_id=customer_id,
                                                    order_id=order.id)
        await call.message.edit_text(f"✅ Вы уверены, что подтверждаете заказ?",
                                     reply_markup=markup)

    elif nav_btn == 'reject':
        markup = await customers_confirmed_order_kb(performer_id=performer.id,
                                                    confirm_type='customer_reject2',
                                                    customer_id=customer_id,
                                                    order_id=order.id)
        await call.message.edit_text(f"❌ Вы уверены, что отклоняете заказ?",
                                     reply_markup=markup)


# Двойное Подтверждение выполнения заказа
@dp.callback_query_handler(customers_confirmed_cd.filter(confirm_type='customer_confirm2'), state="*")
async def double_customer_performed_confirm_order(call: types.CallbackQuery, callback_data: dict,
                                                  state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')
    performer_id = int(callback_data.get('performer_id'))
    customer_id = int(callback_data.get('customer_id'))
    order_id = int(callback_data.get('order_id'))

    performer = await get_user_by_id(performer_id)
    customer = await get_user_by_id(customer_id)

    # Достаем заказ
    order = await get_order_by_id(order_id)

    if nav_btn == 'yes':
        # Удалить заказ в модерации
        await delete_moderate_order(order_id=order_id, user_id=performer_id)

        # Удаление выполнение задания за пользователем
        await delete_reserved_order_to_user(user_id=performer_id, order_id=order_id)

        # Достаем заказ
        order = await get_order_by_id(order_id)

        if order.cashback:
            bonus = order.cashback
        else:
            bonus = 999

        # Увеличить баланс пользователя
        await increase_user_balance(performer_id, bonus)

        # Добавить заказ в "Выполненные"
        await add_performed_order(order_id=order.id, user_id=performer.id)

        markup = await send_to_users_kb()

        await call.message.edit_text("✅ Отлично! Исполнитель получил подтверждение заказа.")

        try:
            await bot.send_message(chat_id=performer.telegram_id,
                                   text=f"✅ Выполнение заказа {order.order_name} подтверждено!\n\n"
                                        f"Вам начислено на баланс - {bonus} руб.",
                                   reply_markup=markup)
        except Exception as ex:
            logger.info(ex)

    elif nav_btn == 'no':
        await call.message.delete()
        await send_to_customers_performed_order(order, customer, performer_id)


# Двойное Отклонение выполнения заказа
@dp.callback_query_handler(customers_confirmed_cd.filter(confirm_type='customer_reject2'), state="*")
async def double_customer_performed_reject_order(call: types.CallbackQuery, callback_data: dict,
                                                 state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')
    performer_id = int(callback_data.get('performer_id'))
    customer_id = int(callback_data.get('customer_id'))
    order_id = int(callback_data.get('order_id'))

    performer = await get_user_by_id(performer_id)
    customer = await get_user_by_id(customer_id)

    # Достаем заказ
    order = await get_order_by_id(order_id)

    if nav_btn == 'yes':
        await call.message.edit_text(f"❌ Исполнитель не получил подтверждение заказа {order.order_name}.\n\n"
                                     f"Связь с админом - @admin")

        try:
            await bot.send_message(chat_id=performer.telegram_id,
                                   text=f"❌ Выполнение заказа {order.order_name} не подтверждено!\n\n"
                                        f"Связь с админом - @admin")
        except Exception as ex:
            logger.info(ex)

    elif nav_btn == 'no':
        await call.message.delete()
        await send_to_customers_performed_order(order, customer, performer_id)
