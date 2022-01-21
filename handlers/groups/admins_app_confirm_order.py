from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsGroups
from keyboards.app_reject_kb import app_reject_kb
from keyboards.inline.app_confirm_kb import app_confirm_kb
from keyboards.inline.callback_datas import admins_confirmed_cd
from loader import dp, bot, scheduler
from utils.db_api.commands.orders_cmds import add_reserved_order_to_user, increase_by_1_orders_total_amount, \
    get_order_by_id, get_reserved_performers_order_by_id
from utils.db_api.commands.users_cmds import get_user_by_id
from utils.one_day_after_take_order import notification_one_day_after_take_order
from loguru import logger


# Подтверждение/Отклонение заявки на бронирование заказа
@dp.callback_query_handler(IsGroups(), admins_confirmed_cd.filter(confirm_type='app_confirm'), state="*")
async def admins_app_confirm_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')
    performer_id = int(callback_data.get('performer_id'))
    order_id = int(callback_data.get('order_id'))

    performer = await get_user_by_id(performer_id)

    if nav_btn == "confirm":  # Подтверждение заявки на бронирование заказа
        # Достаем заказ
        order = await get_order_by_id(order_id)

        if order.goal_amount > order.total_amount:
            # Проверяем или исполнитель не бронировал заказ ранее
            check = await get_reserved_performers_order_by_id(user_id=performer_id, order_id=order_id)

            if not check:
                # Бронируем выполнение задания за пользователем
                reserved_order = await add_reserved_order_to_user(user_id=performer_id, order_id=order_id)

                # Увеличить total_amount заказа на 1
                await increase_by_1_orders_total_amount(order_id=order_id)

                # Уведомление через 24 часа если пользователь не нажал кнопку Выполнено
                scheduler.add_job(func=notification_one_day_after_take_order,
                                  trigger='date', run_date=datetime.now() + timedelta(hours=24),
                                  args=[reserved_order.id],
                                  id=f"24h|{performer_id}-{order_id}")

                markup = await app_confirm_kb()

                # Уведомить пользователя
                try:
                    await bot.send_message(chat_id=performer.telegram_id,
                                           text="✅ Выполнение забронировано за вами!\n\n"
                                                "Перейдите в раздел \"Мои заказы\" - \"Я исполнитель\" - "
                                                "\"Ожидают выполнения\", чтобы продолжить выполнение заказа",
                                           reply_markup=markup)
                except Exception as ex:
                    logger.info(ex)

                await call.message.edit_text(f"✅ Подтверждение заявки на бронирование заказа({order_id}) одобрено!",
                                             reply_markup=None)
            else:
                markup = await app_reject_kb()

                # Уведомить пользователя
                try:
                    await bot.send_message(chat_id=performer.telegram_id,
                                           text=f"❌ Подтверждение заявки на бронирование заказа({order_id}) отклонено!\n\n"
                                                f"Ви уже виполняете этот заказ!",
                                           reply_markup=markup)
                except Exception as ex:
                    logger.info(ex)

                await call.message.edit_text(f"❌ Исполнитерь уже выполняет заказ!",
                                             reply_markup=None)

        else:
            markup = await app_reject_kb()

            # Уведомить пользователя
            try:
                await bot.send_message(chat_id=performer.telegram_id,
                                       text=f"❌ Подтверждение заявки на бронирование заказа({order_id}) отклонено!\n\n"
                                            f"На заказ набралось достаточно исполнителей!",
                                       reply_markup=markup)
            except Exception as ex:
                logger.info(ex)

            await call.message.edit_text(f"❌ На заказ({order_id}) набралось достаточно исполнителей!",
                                         reply_markup=None)

    elif nav_btn == 'reject':
        markup = await app_reject_kb()

        # Уведомить пользователя
        try:
            await bot.send_message(chat_id=performer.telegram_id,
                                   text=f"❌ Подтверждение заявки на бронирование заказа({order_id}) отклонено!\n\n",
                                   reply_markup=markup)
        except Exception as ex:
            logger.info(ex)

        await call.message.edit_text(f"❌ Подтверждение заявки на бронирование заказа({order_id}) отклонена!",
                                     reply_markup=None)
