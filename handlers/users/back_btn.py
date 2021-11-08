from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from handlers.users.balance.balance_menu import balance_menu
from handlers.users.balance.withdrawal_balance import withdrawal_balance
from handlers.users.create_order.create_order_menu import create_order_menu
from handlers.users.create_order.favorites_order import favorites_order, goods_name_favorites_order, \
    goods_link_favorites_order, contacts_favorites_order
from handlers.users.create_order.fire_order import fire_order, goods_name_fire_order, order_description_fire_order, \
    goods_cost_fire_order, goods_link_fire_order, contacts_fire_order, cashback_fire_order
from handlers.users.create_order.redemption_order import redemption_order, goods_name_redemption_order, \
    order_description_redemption_order, goods_cost_redemption_order, goods_link_redemption_order, \
    contacts_redemption_order, cashback_redemption_order
from handlers.users.list_orders.list_orders_menu import list_orders_menu
from handlers.users.main_menu import main_menu
from handlers.users.my_orders.my_orders_customers import my_orders_customers, my_orders_customers_nav
from handlers.users.my_orders.my_orders_performers import my_orders_performers, my_orders_performers_nav, \
    choose_performers_order
from keyboards.inline.callback_datas import back_btn_cd
from loader import dp
from utils.db_api.models import Users


# Нажатия на книпки Назад и тд
@dp.callback_query_handler(NotBanned(), back_btn_cd.filter(), state="*")
async def back_btn(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')

    function = ''

    # Вернуться в главное меню
    if nav_btn == 'main_menu':
        await state.finish()
        function = main_menu

    # Вернуться в меню создание заказа
    elif nav_btn == 'create_order_menu':
        await state.finish()
        function = create_order_menu

    # Просим ввести кол-во выполнений заказа типа 🔥 Выкуп + отзыв + ❤
    elif nav_btn == 'fire_order':
        function = fire_order

    # Просим ввести название товара типа 🔥 Выкуп + отзыв + ❤
    elif nav_btn == 'goods_name_fire_order':
        function = goods_name_fire_order

    # Просим ввести подробное описание заказа типа 🔥 Выкуп + отзыв + ❤
    elif nav_btn == 'order_description_fire_order':
        function = order_description_fire_order

    # Просим ввести стоимость товара типа 🔥 Выкуп + отзыв + ❤
    elif nav_btn == 'goods_cost_fire_order':
        function = goods_cost_fire_order

    # Просим ввести кэшбек типа 🔥 Выкуп + отзыв + ❤
    elif nav_btn == 'cashback_fire_order':
        function = cashback_fire_order

    # Просим ввести ссылку на товар типа 🔥 Выкуп + отзыв + ❤
    elif nav_btn == 'goods_link_fire_order':
        function = goods_link_fire_order

    # Просим контакт для связи типа 🔥 Выкуп + отзыв + ❤
    elif nav_btn == 'contacts_fire_order':
        function = contacts_fire_order

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Просим ввести кол-во выполнений заказа типа 💰 Выкуп
    elif nav_btn == 'redemption_order':
        function = redemption_order

    # Просим ввести название товара типа 💰 Выкуп
    elif nav_btn == 'goods_name_redemption_order':
        function = goods_name_redemption_order

    # Просим ввести подробное описание заказа типа 💰 Выкуп
    elif nav_btn == 'order_description_redemption_order':
        function = order_description_redemption_order

    # Просим ввести стоимость товара типа 💰 Выкуп
    elif nav_btn == 'goods_cost_redemption_order':
        function = goods_cost_redemption_order

    # Просим ввести кэшбек типа 💰 Выкуп
    elif nav_btn == 'cashback_redemption_order':
        function = cashback_redemption_order

    # Просим ввести ссылку на товар типа 💰 Выкуп
    elif nav_btn == 'goods_link_redemption_order':
        function = goods_link_redemption_order

    # Просим контакт для связи типа 💰 Выкуп
    elif nav_btn == 'contacts_redemption_order':
        function = contacts_redemption_order

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Просим ввести кол-во выполнений заказа типа ❤ Избранное
    elif nav_btn == 'favorites_order':
        function = favorites_order

    # Просим ввести название товара типа ❤ Избранное
    elif nav_btn == 'goods_name_favorites_order':
        function = goods_name_favorites_order

    # Просим ввести ссылку на товар типа ❤ Избранное
    elif nav_btn == 'goods_link_favorites_order':
        function = goods_link_favorites_order

    # Просим контакт для связи типа ❤ Избранное
    elif nav_btn == 'contacts_favorites_order':
        function = contacts_favorites_order

    # Мои заказы для заказчика
    elif nav_btn == 'my_orders_customers':
        function = my_orders_customers

    elif nav_btn == 'my_orders_customers_nav':
        function = my_orders_customers_nav

    # Мои заказы для исполнителя
    elif nav_btn == 'my_orders_performers':
        function = my_orders_performers

    elif nav_btn == 'my_orders_performers_nav':
        function = my_orders_performers_nav

    elif nav_btn == 'choose_performers_order':
        function = choose_performers_order

    # Мой баланс
    elif nav_btn == 'balance_menu':
        function = balance_menu

    # Вывести с баланса
    elif nav_btn == 'withdrawal_balance':
        function = withdrawal_balance

    elif nav_btn == 'list_orders_menu':
        function = list_orders_menu

    await function(
        message=call,
        call=call,
        user=user,
        state=state
    )
