import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from handlers.users.balance.balance_menu import paid_for_order
from keyboards.inline.callback_datas import redemption_order_cd, confirm_redemption_order_cd
from keyboards.inline.create_order.cashback_redemption_order_kb import cashback_redemption_order_kb
from keyboards.inline.create_order.confirm_redemption_order_kb import confirm_redemption_order_kb
from keyboards.inline.create_order.contacts_redemption_order_kb import contacts_redemption_order_kb
from keyboards.inline.create_order.goods_cost_redemption_order_kb import goods_cost_redemption_order_kb
from keyboards.inline.create_order.goods_link_redemption_order_kb import goods_link_redemption_order_kb
from keyboards.inline.create_order.goods_name_redemption_order_kb import goods_name_redemption_order_kb
from keyboards.inline.create_order.order_description_redemption_order_kb import order_description_redemption_order_kb
from keyboards.inline.create_order.redemption_order_kb import redemption_order_kb
from loader import dp
from utils.db_api.commands.orders_cmds import add_order, update_order_goal_amount_order_cost_by_id, \
    update_order_goods_name_by_id, update_order_description_by_id, update_order_goods_cost_by_id, \
    update_order_goods_link_by_id, \
    update_order_contacts_by_id, get_order_by_id, update_order_confirmed_by_id, update_order_cashback_by_id
from utils.db_api.commands.price_list_cmds import get_price_by_name
from utils.db_api.models import Users
from re import compile


# 💰 Выкуп
async def redemption_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("redemption_order")

    # Добавляем call в state
    await state.update_data(call=call)

    # Если в state нет id заказа - создаем новый заказ
    if (await state.get_data()).get('current_order_id') is None:
        # Добавление заказа
        order = await add_order(user_id=user.id, type_order='💰')

        # Добавляем order id в state
        await state.update_data(current_order_id=order.id)

    # Получение цены за услугу
    price = (await get_price_by_name(name="💰")).price

    text = f"Услуга: \n" \
           f"🔥 Выкуп + отзыв + избранное\n\n" \
           f"Описание: каждый пользователь выкупает товар\n\n" \
           f"Комиссия сервиса: {price} р за 1 выкуп\n\n" \
           f"👇🏻 Выберите или отправьте сообщением необходимое кол-во выполнений:"

    markup = await redemption_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Навигация в выборе кол-во выполнений 🔥 Выкуп + отзыв + ❤
@dp.callback_query_handler(NotBanned(), redemption_order_cd.filter(), state="redemption_order")
async def redemption_order_nav(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext,
                               **kwargs):
    nav_btn = callback_data.get('nav_btn')
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Получение цены за услугу
    price = (await get_price_by_name(name="💰")).price

    # Стоимость задания
    order_cost = int(nav_btn) * price

    # Обновляем goal_amount заказа
    await update_order_goal_amount_order_cost_by_id(order_id=current_order_id,
                                                    goal_amount=int(nav_btn),
                                                    order_cost=order_cost)

    await goods_name_redemption_order(
        call=call,
        user=user,
        state=state
    )


# Корректный ввод кол-во выполнений с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^\d+$"), state="redemption_order")
async def valid_input_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Получение цены за услугу
    price = (await get_price_by_name(name="💰")).price

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
    await goods_name_redemption_order(call=call, user=user, state=state)


# Некорректный ввод кол-во выполнений с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="redemption_order")
async def invalid_input_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите только число")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим ввести название товара
async def goods_name_redemption_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("goods_name_redemption_order")

    text = f"Услуга: \n" \
           f"💰 Выкуп\n\n" \
           f"👇🏻 Отправьте название товара (до 40 символов)"

    markup = await goods_name_redemption_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Корректный ввод названия товара с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^.{0,40}$"), state="goods_name_redemption_order")
async def valid_input_goods_name_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Название товара
    goods_name = message.text
    await message.delete()

    # Обновляем goods_name заказа
    await update_order_goods_name_by_id(order_id=current_order_id, goods_name=goods_name)

    # Просим ввести подробное опизание заказа
    await order_description_redemption_order(call=call, user=user, state=state)


# Некорректный ввод названия товара с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="goods_name_redemption_order")
async def invalid_input_goods_name_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите название товара")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим ввести подробное описание заказа
async def order_description_redemption_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("order_description_redemption_order")

    text = f"Услуга: \n" \
           f"💰 Выкуп\n\n" \
           f"👇🏻 Отправьте подробное описание задания (до 400 символов)\n\n" \
           f"К примеру:\n" \
           f"\"Выкупить товар\""

    markup = await order_description_redemption_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Корректный ввод описание заказа с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^.{0,400}$"), state="order_description_redemption_order")
async def valid_input_order_description_redemption_order(message: types.Message, user: Users, state: FSMContext,
                                                         **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Описание заказа
    order_description = message.text
    await message.delete()

    # Обновляем order_description заказа
    await update_order_description_by_id(order_id=current_order_id, order_description=order_description)

    # Просим ввести цену товара
    await goods_cost_redemption_order(call=call, user=user, state=state)


# Некорректный ввод описание заказа с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="order_description_redemption_order")
async def invalid_input_order_description_redemption_order(message: types.Message, user: Users, state: FSMContext,
                                                           **kwargs):
    error_msg = await message.answer("Пожалуйста, введите описание заказа")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим ввести стоимость товара
async def goods_cost_redemption_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("goods_cost_redemption_order")

    text = f"Услуга: \n" \
           f"💰 Выкуп\n\n" \
           f"👇🏻 Отправьте цену товара (только число)"

    markup = await goods_cost_redemption_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Корректный ввод стоимости товара с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^\d*$"), state="goods_cost_redemption_order")
async def valid_input_goods_cost_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Стоимость товара
    goods_cost = int(message.text)
    await message.delete()

    # Обновляем order_description заказа
    await update_order_goods_cost_by_id(order_id=current_order_id, goods_cost=goods_cost)

    # Просим ввести кэшбек
    await cashback_redemption_order(call=call, user=user, state=state)


# Некорректный ввод стоимости товара с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="goods_cost_redemption_order")
async def invalid_input_goods_cost_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите только число")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим ввести кэшбек
async def cashback_redemption_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("cashback_redemption_order")

    text = f"Услуга: \n" \
           f"💰 Выкуп\n\n" \
           f"👇🏻 Отправьте кэшбек товара (только число от 50% и до 100%)"

    markup = await cashback_redemption_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Корректный ввод кэшбека с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^([5-9][\d]|100)$"), state="cashback_redemption_order")
async def valid_input_cashback_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Кэшбек/скидка
    cashback = int(message.text)
    await message.delete()

    # Обновляем cashback заказа
    await update_order_cashback_by_id(order_id=current_order_id, cashback=cashback)

    # Просим ввести ссылку на товар
    await goods_link_redemption_order(call=call, user=user, state=state)


# Некорректный ввод кэшбека с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="cashback_redemption_order")
async def invalid_input_cashback_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите только число от 50 до 100")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим ввести ссылку на товар
async def goods_link_redemption_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("goods_link_redemption_order")

    text = f"Услуга: \n" \
           f"💰 Выкуп\n\n" \
           f" Отправьте ссылку на товар на Wildberries:\n\n" \
           f"Примеры ссылок:\n" \
           f"1) https://www.wildberries.ru/catalog/13724854/detail.aspx?targetUrl=MI \n" \
           f"2) www.wildberries.ru/catalog/13724854/detail.aspx?targetUrl=MI\n" \
           f"3) wildberries.ru/catalog/13724854/detail.aspx?targetUrl=MI"

    markup = await goods_link_redemption_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup, disable_web_page_preview=True)


# Корректный ввод ссылки на товар с клавиатуры
@dp.message_handler(NotBanned(), state="goods_link_redemption_order")
async def valid_input_goods_link_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Ссылка на товар
    goods_link = message.text
    await message.delete()

    # Обновляем goods_link заказа
    await update_order_goods_link_by_id(order_id=current_order_id, goods_link=goods_link)

    # Просим контакт для связи
    await contacts_redemption_order(call=call, user=user, state=state)


# Некорректный ввод ссылки на товар с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="goods_link_redemption_order")
async def invalid_input_goods_link_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите ссылку на товар")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим контакт для связи
async def contacts_redemption_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("contacts_redemption_order")

    text = f"Услуга: \n" \
           f"💰 Выкуп\n\n" \
           f"Введите номер телефона. Примеры ввода:\n" \
           f"+7(903)888-88-88\n" \
           f"8(999)99-999-99\n" \
           f"+380(67)777-7-777\n" \
           f"001-541-754-3010\n" \
           f"+1-541-754-3010\n" \
           f"19-49-89-636-48018\n" \
           f"+233 205599853"

    markup = await contacts_redemption_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Корректный ввод номера телефона с клавиатуры
@dp.message_handler(NotBanned(), regexp=compile(r"^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$"),
                    state="contacts_redemption_order")
async def valid_input_contacts_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    call: types.CallbackQuery = (await state.get_data()).get("call")
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Новер телефона
    contacts = message.text
    await message.delete()

    # Обновляем goods_link заказа
    await update_order_contacts_by_id(order_id=current_order_id, contacts=contacts)

    # Просим подтвердить заказ
    await confirm_redemption_order(call=call, user=user, state=state)


# Некорректный ввод номера телефона с клавиатуры
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="contacts_redemption_order")
async def invalid_input_contacts_redemption_order(message: types.Message, user: Users, state: FSMContext, **kwargs):
    error_msg = await message.answer("Пожалуйста, введите действительный номер телефона")
    await asyncio.sleep(5)
    await message.delete()
    await error_msg.delete()


# Просим подтвердить заказ
async def confirm_redemption_order(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    await state.set_state("confirm_redemption_order")

    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Получение цены за услугу
    price = (await get_price_by_name(name="💰")).price

    # Получение заказа
    order = await get_order_by_id(order_id=current_order_id)

    text = f"ПОДТВЕРДИТЕ ДАННЫЕ:\n\n" \
           f"Услуга:\n" \
           f"💰 Выкуп\n\n" \
           f"❤️ Комиссия сервиса за 1 услугу: {price} руб.\n" \
           f"🧮 Вы заказали количество: {order.goal_amount} шт.\n" \
           f"Кэшбек/скидка: {order.cashback}%\n" \
           f"Цена товара: {order.goods_cost} рублей\n" \
           f"💳 Общая стоимость услуги: {order.order_cost} рублей\n\n" \
           f"Название товара:\n" \
           f"{order.goods_name}\n\n" \
           f"Комментарии по заказу:\n" \
           f"{order.order_description}\n\n" \
           f"Ссылка на товар:\n" \
           f"{order.goods_link}\n\n" \
           f"Контакт для связи:\n" \
           f"{order.contacts}"

    markup = await confirm_redemption_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Подтверждение заказа 💰 Выкуп
@dp.callback_query_handler(NotBanned(), confirm_redemption_order_cd.filter(), state="confirm_redemption_order")
async def confirm_redemption_order_nav(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext,
                                       **kwargs):
    current_order_id = int((await state.get_data()).get("current_order_id"))

    # Обновляем confirmed заказа
    await update_order_confirmed_by_id(order_id=current_order_id, confirmed=True)

    # Перенеправление на оплату товара
    await paid_for_order(call=call, user=user, state=state)
