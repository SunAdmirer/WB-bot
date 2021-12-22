from datetime import datetime, timedelta
from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from keyboards.inline.callback_datas import list_orders_cd
from keyboards.inline.list_orders.confirm_execute_order_kb import confirm_execute_order_kb
from keyboards.inline.list_orders.execute_order_kb import execute_order_kb
from keyboards.inline.list_orders.performer_with_orders_kb import performer_with_orders_kb
from keyboards.inline.list_orders.performer_without_orders_kb import performer_without_orders_kb
from keyboards.inline.list_orders.show_order_kb import show_order_kb
from loader import dp
from utils.db_api.commands.orders_cmds import get_confirmed_paid_for_orders, get_performed_performers_orders, \
    get_reserved_performers_orders_, get_confirmed_paid_for_orders_by_type, add_reserved_order_to_user, \
    increase_by_1_orders_total_amount, get_order_by_id
from utils.db_api.models import Users, Orders
from utils.misc.functions import check_order_if_suitable
from utils.send_to_admins_app_order import send_to_admins_app_order


async def list_orders_menu(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    # Получаем все задания 🔥 Выкуп + отзыв + ❤, которые подтвердили и оплатили, но еще не выполненные
    fire_orders = await get_confirmed_paid_for_orders_by_type(type_order="🔥")

    # Получаем все задания ❤ Избранное, которые подтвердили и оплатили, но еще не выполненные
    favorites_orders = await get_confirmed_paid_for_orders_by_type(type_order="❤")

    # Получаем все задания 💰 Выкуп, которые подтвердили и оплатили, но еще не выполненные
    redemption_orders = await get_confirmed_paid_for_orders_by_type(type_order="💰")

    # Получаем выполненные задания исполнителя
    performed_orders = await get_performed_performers_orders(user_id=user.id)

    # Получаем задания что ожидают выполнения
    reserved_orders = await get_reserved_performers_orders_(user_id=user.id)

    for orders in [fire_orders, favorites_orders, redemption_orders]:
        # Фильтруем те задания, которые пользователь уже выполнил
        orders[:] = [order for order in orders if await check_order_if_suitable(order, performed_orders)]

        # Фильтруем те задания, которые пользователь зарезервировал
        orders[:] = [order for order in orders if await check_order_if_suitable(order, reserved_orders)]

    await state.update_data(favorites_orders=favorites_orders,
                            redemption_orders=redemption_orders,
                            fire_orders=fire_orders)

    # Для пользователя есть задания
    if fire_orders or favorites_orders or redemption_orders:
        text = f"🤑 Выбери задания\n\n" \
               f"👇🏻 Выбери задания"

        markup = await performer_with_orders_kb()

    else:
        await orders_ended_warning(call=call, user=user, state=state)
        return

    await call.message.edit_text(text=text, reply_markup=markup)


async def show_order(call: types.CallbackQuery, user: Users, state: FSMContext, type_order: str, order_id, **kwargs):
    data = await state.get_data()

    if type_order == '🔥':
        fire_orders: List[Orders] = data.get('fire_orders')

        if fire_orders or order_id != '-':
            if order_id != '-':
                # Текущее задание
                current_order = await get_order_by_id(int(order_id))
            else:
                # Текущее задание
                current_order = fire_orders.pop(0)
                await state.update_data(fire_orders=fire_orders)

            text = f"Услуга:\n" \
                   f"🔥 Выкуп + отзыв + избранное\n\n" \
                   f"Цена товара: {current_order.goods_cost} рублей\n" \
                   f"🧮 Кэшбек/скидка: {current_order.cashback} рублей\n" \
                   f"💳 Ваша награда: 2 балла + товар\n\n" \
                   f"Название товара:\n{current_order.goods_name}\n\n" \
                   f"Комментарии по заказу:\n{current_order.order_description}\n\n" \
                   f"⚠️ ВАЖНО!\n" \
                   f"-Оставить положительный отзыв с оценкой ⭐⭐⭐⭐⭐ и с фото 📸\n\n" \
                   f"⚠️ ВАЖНО!\n" \
                   f"-Добавь бренд и товар в избранное - отметь ♥️ на странице бренда и в карточке товара.\n\n" \
                   f"⚠️ ВАЖНО!\n" \
                   f"-Товар не возвращать. Дабы не снизить %%% выкупа.\n\n" \
                   f"⚠️ ВАЖНО!\n" \
                   f"-Один товар в одни руки.\n\n" \
                   f"Ссылка на товар:\n{current_order.goods_link}\n\n" \
                   f"Если у вас возникли вопросы или вы хотите пожаловаться " \
                   f"на товар, напишите в тех. поддержку 👉🏻 @support"

            markup = await show_order_kb(type_order=type_order, url=current_order.goods_link,
                                         order_id=current_order.id)
        else:
            await orders_ended_warning(call=call, user=user, state=state)
            return

    elif type_order == '❤':
        favorites_orders: List[Orders] = data.get('favorites_orders')

        if favorites_orders or order_id != '-':
            if order_id != '-':
                # Текущее задание
                current_order = await get_order_by_id(int(order_id))
            else:
                # Текущее задание
                current_order = favorites_orders.pop(0)

                await state.update_data(favorites_orders=favorites_orders)

            text = f"Услуга:\n" \
                   f"❤ Избранное\n\n" \
                   f"💳 Ваша награда: 2 балла + товар\n\n" \
                   f"Название товара:\n{current_order.goods_name}\n\n" \
                   f"Комментарии по заказу:\n{current_order.order_description}\n\n" \
                   f"⚠️ ВАЖНО!\n" \
                   f"-Добавь бренд и товар в избранное - отметь ♥️ на странице бренда и в карточке товара.\n\n" \
                   f"Ссылка на товар:\n{current_order.goods_link}\n\n" \
                   f"Если у вас возникли вопросы или вы хотите пожаловаться " \
                   f"на товар, напишите в тех. поддержку 👉🏻 @support"

            markup = await show_order_kb(type_order=type_order, url=current_order.goods_link,
                                         order_id=current_order.id)
        else:
            await orders_ended_warning(call=call, user=user, state=state)
            return

    else:
        redemption_orders: List[Orders] = data.get('redemption_orders')

        if redemption_orders or order_id != '-':
            if order_id != '-':
                # Текущее задание
                current_order = await get_order_by_id(int(order_id))
            else:
                # Текущее задание
                current_order = redemption_orders.pop(0)

                await state.update_data(redemption_orders=redemption_orders)

            text = f"Услуга:\n" \
                   f"💰 Выкуп\n\n" \
                   f"Цена товара: {current_order.goods_cost} рублей\n" \
                   f"🧮 Кэшбек/скидка: {current_order.cashback} рублей\n" \
                   f"💳 Ваша награда: 2 балла + товар\n\n" \
                   f"Название товара:\n{current_order.goods_name}\n\n" \
                   f"Комментарии по заказу:\n{current_order.order_description}\n\n" \
                   f"⚠️ ВАЖНО!\n" \
                   f"-Товар не возвращать. Дабы не снизить %%% выкупа.\n\n" \
                   f"⚠️ ВАЖНО!\n" \
                   f"-Один товар в одни руки.\n\n" \
                   f"Ссылка на товар:\n{current_order.goods_link}\n\n" \
                   f"Если у вас возникли вопросы или вы хотите пожаловаться " \
                   f"на товар, напишите в тех. поддержку 👉🏻 @support"

            markup = await show_order_kb(type_order=type_order, url=current_order.goods_link,
                                         order_id=current_order.id)
        else:
            await orders_ended_warning(call=call, user=user, state=state)
            return

    await call.message.edit_text(text=text, reply_markup=markup, disable_web_page_preview=True)


async def execute_order(call: types.CallbackQuery, user: Users, state: FSMContext,
                        type_order: str, order_id: int, **kwargs):
    current_order = await get_order_by_id(order_id)

    execute_date = (datetime.now() - timedelta(days=7)).date()

    text = f"Внимание! Если вы нажимаете кнопку \"Выполнить\"," \
           f" то подтверждаете, что выполнение задания будет" \
           f" сделано в течение 7 дней до {execute_date}?\n\n" \
           f"❗ За вами зафиксируется место, и если задание" \
           f" не будет выполнено, то ваш аккаунт попадает в бан.\n\n" \
           "❗Обратите внимание на условия возврата.\n\n" \
           "❗Проверьте, не заказывали ли ранее товар.\n\n" \
           "❗После подтверждения за вами зафиксируется место" \
           " и если задание не будет выполнено, то ваш аккаунт попадет в бан на время.\n\n" \
           "Подтверждаете, что выполните задание в течение 7 дней?"

    markup = await execute_order_kb(order_id=order_id, type_order=current_order.type_order)

    await call.message.edit_text(text=text, reply_markup=markup)


async def confirm_execute_order(call: types.CallbackQuery, user: Users, state: FSMContext, order_id: int, **kwargs):
    markup = await confirm_execute_order_kb()

    # Достаем заказ
    order = await get_order_by_id(order_id)

    # Заявка на бронирование заказа в чат админов
    await send_to_admins_app_order(order=order, performer=user)

    await call.message.edit_text(text="Заявка на бронирование заказа отослана на модерацию.\n\n"
                                      "Скоро с вами свяжется администратор",
                                 reply_markup=markup)


@dp.callback_query_handler(NotBanned(), list_orders_cd.filter(), state="*")
async def list_orders_menu_nav(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext,
                               **kwargs):
    nav_btn = callback_data.get('nav_btn')
    order_id = callback_data.get('order_id')

    function = ''

    if nav_btn in "🔥❤💰":
        function = show_order

    elif nav_btn == 'execute':
        order_id = int(order_id)
        function = execute_order

    elif nav_btn == 'confirm':
        order_id = int(order_id)
        function = confirm_execute_order

    await function(
        call=call,
        user=user,
        state=state,
        type_order=nav_btn,
        order_id=order_id
    )


async def orders_ended_warning(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    text = "😔 К сожалению задания закончились.\n" \
           "Хотите включить уведомления о новых заданиях?\n\n" \
           "Если у вас возникли вопросы, напишите в тех. поддержку 👉🏻 @support"

    markup = await performer_without_orders_kb()

    await call.message.edit_text(text=text, reply_markup=markup)
