import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsGroups
from keyboards.inline.callback_datas import admins_confirmed_cd
from keyboards.inline.send_to_admins_kb import admins_performed_confirm_order_kb, reject_double_confirmed
from keyboards.inline.send_to_users_kb import send_to_users_kb
from loader import dp, bot
from utils.db_api.commands.orders_cmds import get_order_by_id, update_moderate_order_confirmed, \
    get_moderate_performers_order, get_media_content, decrease_by_1_orders_total_amount, delete_reserved_order_to_user, \
    delete_moderate_order

from utils.db_api.commands.users_cmds import get_user_by_id
from utils.send_to_admins_performed_order import send_to_admins_performed_order
from utils.send_to_customers_media import send_to_customers_media
from utils.send_to_customers_performed_order import send_to_customers_performed_order
from loguru import logger


# Подтверждение/Отклонение выполнения заказа
@dp.callback_query_handler(IsGroups(), admins_confirmed_cd.filter(confirm_type='performed_confirm'), state="*")
async def admins_performed_confirm_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')
    performer_id = int(callback_data.get('performer_id'))
    customer_id = int(callback_data.get('customer_id'))
    order_id = int(callback_data.get('order_id'))

    performer = await get_user_by_id(performer_id)

    # Достаем заказ
    order = await get_order_by_id(order_id)

    if nav_btn == 'confirm':
        markup = await admins_performed_confirm_order_kb(performer_id=performer.id,
                                                         confirm_type='confirm2',
                                                         customer_id=customer_id,
                                                         order_id=order.id)
        await call.message.edit_text(f"✅ Вы уверены, что подтверждаете заказ?",
                                     reply_markup=markup)

    elif nav_btn == 'reject':
        markup = await admins_performed_confirm_order_kb(performer_id=performer.id,
                                                         confirm_type='reject2',
                                                         customer_id=customer_id,
                                                         order_id=order.id)
        await call.message.edit_text(f"❌ Вы уверены, что отклоняете заказ?",
                                     reply_markup=markup)


# Двойное Подтверждение выполнения заказа
@dp.callback_query_handler(IsGroups(), admins_confirmed_cd.filter(confirm_type='confirm2'), state="*")
async def double_admins_performed_confirm_order(call: types.CallbackQuery, callback_data: dict,
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
        # Достаем задание на модерации исполнителя
        moderate_order = await get_moderate_performers_order(performer_id=performer_id, order_id=order_id)

        # Достаем фото для заказа в модерации исполнителя
        media_content = await get_media_content(moderate_order_id=moderate_order.id)

        media = types.MediaGroup()

        for content in media_content:
            media.attach_photo(content.file_id)

        # Достаем заказчика
        customer = await get_user_by_id(user_id=order.user_id)

        # Админ подтверждает выполнение
        await update_moderate_order_confirmed(order_id=order_id, confirmed=True)

        # Отправляем скриншоты заказчику
        await send_to_customers_media(media=media, customer=customer)

        # Отправляем выполненное задание заказчику
        await send_to_customers_performed_order(order=order, customer=customer, performer_id=performer_id)

        await call.message.edit_text("✅ Отлично! Исполнитель получил подтверждение заказа.")

        markup = await send_to_users_kb()

        try:
            await bot.send_message(chat_id=performer.telegram_id,
                                   text=f"✅ Выполнение заказа {order.order_name} подтверждено админом!",
                                   reply_markup=markup)
        except Exception as ex:
            logger.info(ex)

    elif nav_btn == 'no':
        await call.message.delete()
        await send_to_admins_performed_order(order, performer, customer)


# Двойное Отклонение выполнения заказа
@dp.callback_query_handler(IsGroups(), admins_confirmed_cd.filter(confirm_type='reject2'), state="*")
async def double_admins_performed_reject_order(call: types.CallbackQuery, callback_data: dict,
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
        await call.message.edit_text("❌ Выполнение задания не подтверждено")

        # Уменьшить total_amount заказа на 1
        await decrease_by_1_orders_total_amount(order_id=order_id)

        # Удаление выполнение задания за пользователем
        await delete_reserved_order_to_user(user_id=performer_id, order_id=order_id)

        # Удалить заказ в модерации
        await delete_moderate_order(order_id=order_id, user_id=performer_id)

        markup = await send_to_users_kb()

        try:
            await bot.send_message(chat_id=performer.telegram_id,
                                   text=f"❌ Выполнение заказа {order.order_name} не подтверждено админом!",
                                   reply_markup=markup)
        except Exception as ex:
            logger.info(ex)

    elif nav_btn == 'no':
        await call.message.delete()
        await send_to_admins_performed_order(order, performer, customer)
