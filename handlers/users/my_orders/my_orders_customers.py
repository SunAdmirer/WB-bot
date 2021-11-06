from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from keyboards.inline.my_orders.choose_customers_orders_kb import choose_customers_orders_kb
from keyboards.inline.callback_datas import customers_with_orders_cd, paginator_customers_cd, choose_customers_orders_cd
from keyboards.inline.my_orders.choose_customers_order_kb import choose_customers_order_kb
from keyboards.inline.my_orders.customers_with_orders_kb import customers_with_orders_kb
from keyboards.inline.my_orders.customers_without_orders_kb import customers_without_orders_kb
from loader import dp
from utils.db_api.commands.orders_cmds import check_is_customers_orders, get_count_performed_orders, \
    get_count_in_process_orders, get_performed_customers_orders, get_in_process_customers_orders, get_order_by_id
from utils.db_api.commands.price_list_cmds import get_price_by_name
from utils.db_api.models import Users


@dp.callback_query_handler(NotBanned(), text="customer", state="*")
async def my_orders_customers(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    # Проверяем есть ли у заказчика заказы
    check = await check_is_customers_orders(user_id=user.id)

    if check:
        # Получаем кол-во выполненных заказов заказчика
        count_performed_orders = await get_count_performed_orders(user_id=user.id)

        # Получаем кол-во заказов в процессе заказчика
        count_in_process_orders = await get_count_in_process_orders(user_id=user.id)

        text = "🛒 Мои заказы\n\n" \
               f"✅ Выполненные: {count_performed_orders} шт.\n" \
               f"⏳ В процессе выполнения: {count_in_process_orders} шт."

        markup = await customers_with_orders_kb(performed=count_performed_orders,
                                                in_process=count_in_process_orders)

    else:
        text = "🛒 Мои заказы\n\n" \
               "🤷‍♂️ У вас нет заказов.\n\n" \
               "Хотите создать первый заказ?"

        markup = await customers_without_orders_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(NotBanned(), customers_with_orders_cd.filter(), state="*")
async def my_orders_customers_nav(call: types.CallbackQuery, user: Users,
                                  state: FSMContext, callback_data: dict = None, **kwargs):
    if callback_data:
        nav_btn = callback_data.get('nav_btn')
        await state.update_data(order_type=nav_btn)
    else:
        nav_btn = (await state.get_data()).get("order_type")

    if nav_btn == "performed":
        # Получаем кол-во выполненных заказов заказчика
        count_performed_orders = await get_count_performed_orders(user_id=user.id)

        # Получаем выполненные задания заказчика
        orders = await get_performed_customers_orders(user_id=user.id)

        text = f"✅ Мои выполненные заказы: {count_performed_orders} шт.\n\n" \
               f"👇🏻 Узнать подробную информацию о заказе..."

        markup = await choose_customers_orders_kb(type_order='performed', orders=orders)

    else:
        # Получаем кол-во заказов в процессе заказчика
        count_in_process_orders = await get_count_in_process_orders(user_id=user.id)

        # Получаем задания в процессе заказчика
        orders = await get_in_process_customers_orders(user_id=user.id)

        text = f"⏳ Мои заказы в процессе выполнения: {count_in_process_orders} шт.\n\n" \
               f"👇🏻 Узнать подробную информацию о заказе..."

        markup = await choose_customers_orders_kb(type_order='in_process', orders=orders)

    await call.message.edit_text(text=text, reply_markup=markup)


# Пагинатор для заданий
@dp.callback_query_handler(paginator_customers_cd.filter(), state="*")
async def paginator_orders(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext):
    current_page = int(callback_data.get("page"))
    type_order = callback_data.get("type_order")

    if type_order == "performed":
        # Получаем выполненные задания заказчика
        orders = await get_performed_customers_orders(user_id=user.id)
    else:
        # Получаем задания в процессе заказчика
        orders = await get_in_process_customers_orders(user_id=user.id)

    markup = await choose_customers_orders_kb(type_order=type_order, orders=orders, page=current_page)
    await call.message.edit_reply_markup(reply_markup=markup)


# Выбранное задание
@dp.callback_query_handler(choose_customers_orders_cd.filter(), state="*")
async def choose_customers_order(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext):
    order_id = int(callback_data.get("order"))

    # Получение заказа по id
    order = await get_order_by_id(order_id=order_id)

    if order.performed:
        order_performed = "✅ выполнен"
    else:
        order_performed = "⏳ в процессе выполнения"

    if order.type_order == "🔥":
        type_order = "🔥 Выкуп + отзыв + избранное"
        # Получение цены за услугу
        price = (await get_price_by_name(name="🔥")).price

    elif order.type_order == "💰":
        type_order = "💰 Выкуп"
        # Получение цены за услугу
        price = (await get_price_by_name(name="💰")).price

    else:
        type_order = "❤ Избранное"
        # Получение цены за услугу
        price = (await get_price_by_name(name="❤")).price

    text = f"🔽🔽🔽 Заказ {order.order_name} 🔽🔽🔽\n\n" \
           f"Услуга - {type_order}\n\n" \
           f"❤️ Комиссия сервиса за 1 услугу: {price} руб.\n" \
           f"🧮 Вы заказали количество: {order.goal_amount} шт.\n" \
           f"💳 Общая стоимость услуги: {order.order_cost} рублей\n\n" \
           f"Ссылка на товар:\n" \
           f"{order.goods_link}\n\n" \
           f"Статус заказа: {order_performed}."

    markup = await choose_customers_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)
