import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from handlers.users.balance.balance_menu import paid_for_order
from keyboards.inline.callback_datas import favorites_order_cd, confirm_favorites_order_cd
from keyboards.inline.create_order.confirm_favorites_order_kb import confirm_favorites_order_kb
from keyboards.inline.create_order.contacts_favorites_order_kb import contacts_favorites_order_kb
from keyboards.inline.create_order.favorites_order_kb import favorites_order_kb
from keyboards.inline.create_order.goods_link_favorites_order_kb import goods_link_favorites_order_kb
from keyboards.inline.create_order.goods_name_favorites_order_kb import goods_name_favorites_order_kb
from loader import dp
from utils.db_api.commands.orders_cmds import add_order, update_order_goal_amount_order_cost_by_id, \
    update_order_goods_name_by_id, update_order_goods_link_by_id, update_order_contacts_by_id, get_order_by_id, \
    update_order_confirmed_by_id
from utils.db_api.commands.price_list_cmds import get_price_by_name
from utils.db_api.models import Users
from re import compile


# ❤ Избранное
async def favorites_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("favorites_order")

    # Добавляем call в state
    await state.update_data(call=call)

    # Если в state нет id заказа - создаем новый заказ
    if (await state.get_data()).get('current_order_id') is None:
        # Добавление заказа
        order = await add_order(user_id=user.id, type_order='❤')

        # Добавляем order id в state
        await state.update_data(current_order_id=order.id)

    # Получение цены за услугу
    price = (await get_price_by_name(name="❤")).price

    text = f"Услуга: \n" \
           f"❤ Избранное\n\n" \
           f"Описание: каждый пользователь добавляет товар в избранное.\n\n" \
           f"Комиссия сервиса: {price} р за 1 добавление в избранное\n\n" \
           f"👇🏻 Выберите или отправьте сообщением необходимое кол-во выполнений:"

    markup = await favorites_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Навигация в выборе кол-во выполнений ❤ Избранное
@dp.callback_query_handler(NotBanned(), favorites_order_cd.filter(), state="favorites_order")
async def favorites_order_nav(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext,
                              **kwargs):
    nav_btn = callback_data.get('nav_btn')
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Получение цены за услугу
    price = (await get_price_by_name(name="❤")).price

    # Стоимость задания
    order_cost = int(nav_btn) * price

    # Обновляем goal_amount заказа
    await update_order_goal_amount_order_cost_by_id(order_id=current_order_id,
                                                    goal_amount=int(nav_btn),
                                                    order_cost=order_cost)

    await goods_name_favorites_order(
        call=call,
        user=user,
        state=state
    )


# Корректный ввод кол-во выполнений с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^\d+$"), state="favorites_order")
async def valid_input_favorites_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Получение цены за услугу
    price = (await get_price_by_name(name="❤")).price

    # Кол-во выполнений
    goal_amount = int(message.text)
    await message.delete()

    # Стоимость задания
    order_cost = goal_amount * price

    # Обновляем goal_amount заказа
    await update_order_goal_amount_order_cost_by_id(order_id=current_order_id,
                                                    goal_amount=goal_amount,
                                                    order_cost=order_cost)

    # Просим ввести название товара
    await goods_name_favorites_order(call=call, user=user, state=state)


# Некорректный ввод кол-во выполнений с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="favorites_order")
async def invalid_input_favorites_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите только число")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим ввести название товара
async def goods_name_favorites_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("goods_name_favorites_order")

    text = f"Услуга: \n" \
           f"❤ Избранное\n\n" \
           f"👇🏻 Отправьте название товара (до 40 символов)"

    markup = await goods_name_favorites_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Корректный ввод названия товара с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^.{0,40}$"), state="goods_name_favorites_order")
async def valid_input_goods_name_favorites_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Название товара
    goods_name = message.text
    await message.delete()

    # Обновляем goods_name заказа
    await update_order_goods_name_by_id(order_id=current_order_id, goods_name=goods_name)

    # Просим ввести ссылку на товар
    await goods_link_favorites_order(call=call, user=user, state=state)


# Некорректный ввод названия товара с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^.{40,4000}$"), state="goods_name_favorites_order")
async def invalid_input_goods_name_favorites_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите название не больше 40 символов.")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Некорректный ввод названия товара с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="goods_name_favorites_order")
async def invalid_input_goods_name_favorites_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите название товара")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим ввести ссылку на товар
async def goods_link_favorites_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("goods_link_favorites_order")

    text = f"Услуга: \n" \
           f"❤ Избранное\n\n" \
           f" Отправьте ссылку на товар на Wildberries:\n\n" \
           f"Примеры ссылок:\n" \
           f"1) https://www.wildberries.ru/catalog/13724854/detail.aspx?targetUrl=MI \n" \
           f"2) www.wildberries.ru/catalog/13724854/detail.aspx?targetUrl=MI\n" \
           f"3) wildberries.ru/catalog/13724854/detail.aspx?targetUrl=MI"

    markup = await goods_link_favorites_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup, disable_web_page_preview=True)


# Корректный ввод ссылки на товар с клавиатуры
@dp.message_handler(NotBanned(), state="goods_link_favorites_order")
async def valid_input_goods_link_favorites_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Ссылка на товар
    goods_link = message.text
    await message.delete()

    # Обновляем goods_link заказа
    await update_order_goods_link_by_id(order_id=current_order_id, goods_link=goods_link)

    # Просим контакт для связи
    await contacts_favorites_order(call=call, user=user, state=state)


# Некорректный ввод ссылки на товар с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="goods_link_favorites_order")
async def invalid_input_goods_link_favorites_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите ссылку на товар")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим контакт для связи
async def contacts_favorites_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("contacts_favorites_order")

    text = f"Услуга: \n" \
           f"❤ Избранное\n\n" \
           f"Введите номер телефона. Примеры ввода:\n" \
           f"89999999999\n" \
           f"+79999999999\n"

    markup = await contacts_favorites_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Корректный ввод номера телефона с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^\+?\d{0,20}$"),
                    state="contacts_favorites_order")
async def valid_input_contacts_favorites_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Новер телефона
    contacts = message.text
    await message.delete()

    # Обновляем goods_link заказа
    await update_order_contacts_by_id(order_id=current_order_id, contacts=contacts)

    # Просим подтвердить заказ
    await confirm_favorites_order(call=call, user=user, state=state)


# Некорректный ввод номера телефона с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="contacts_favorites_order")
async def invalid_input_contacts_favorites_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите действительный номер телефона")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим подтвердить заказ
async def confirm_favorites_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("confirm_favorites_order")

    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Получение цены за услугу
    price = (await get_price_by_name(name="❤")).price

    # Получение заказа
    order = await get_order_by_id(order_id=current_order_id)

    text = f"<b>ПОДТВЕРДИТЕ ДАННЫЕ:</b>\n\n" \
           f"Услуга:\n" \
           f"❤ Избранное\n\n" \
           f"❤️ Комиссия сервиса за 1 услугу: {price} руб.\n" \
           f"🧮 Вы заказали количество: {order.goal_amount} шт.\n" \
           f"Цена товара: {order.goods_cost} рублей\n" \
           f"💳 Общая стоимость услуги: {order.order_cost} рублей\n\n" \
           f"Название товара:\n" \
           f"{order.goods_name}\n\n" \
           f"Ссылка на товар:\n" \
           f"{order.goods_link}\n\n" \
           f"Контакт для связи:\n" \
           f"{order.contacts}"

    markup = await confirm_favorites_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Подтверждение заказа ❤ Избранное
@dp.callback_query_handler(NotBanned(), confirm_favorites_order_cd.filter(), state="confirm_favorites_order")
async def confirm_favorites_order_nav(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext,
                                      **kwargs):
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Обновляем confirmed заказа
    await update_order_confirmed_by_id(order_id=current_order_id, confirmed=True)

    # Перенеправление на оплату товара
    await paid_for_order(call=call, user=user, state=state)
