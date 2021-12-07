import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from filters import NotBanned
from keyboards.inline.callback_datas import performers_with_orders_cd, paginator_performers_cd, \
    choose_performers_orders_cd, chosen_performers_reserved_order_cd, check_for_execution_cd
from keyboards.inline.my_orders.check_for_execution_kb import check_for_execution_kb
from keyboards.inline.my_orders.choose_performers_order_kb import choose_performers_order_kb
from keyboards.inline.my_orders.choose_performers_orders_kb import choose_performers_orders_kb
from keyboards.inline.my_orders.choose_performers_reserved_order_kb import choose_performers_reserved_order_kb
from keyboards.inline.my_orders.confirm_screenshots_kb import confirm_screenshots_kb
from keyboards.inline.my_orders.performers_with_orders_kb import performers_with_orders_kb
from keyboards.inline.my_orders.performers_without_orders_kb import performers_without_orders_kb
from loader import dp, bot, scheduler
from utils.db_api.commands.orders_cmds import check_is_performers_orders, get_count_performed_orders_performer, \
    get_count_moderate_orders, get_count_reserved_orders, get_performed_performers_orders, \
    get_reserved_performers_orders, get_moderate_performers_orders, get_order_by_id, add_moderate_order, \
    add_media_content
from utils.db_api.commands.price_list_cmds import get_price_by_name
from utils.db_api.commands.users_cmds import get_user_by_id, get_user_by_telegram_id
from utils.db_api.models import Users
from utils.send_to_admins_media import send_to_admins_media
from utils.send_to_admins_performed_order import send_to_admins_performed_order
from utils.send_to_customers_media import send_to_customers_media
from utils.send_to_customers_performed_order import send_to_customers_performed_order


@dp.callback_query_handler(NotBanned(), text="performer", state="*")
async def my_orders_performers(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    # Проверяем есть ли у исполнителя заказы
    check = await check_is_performers_orders(user_id=user.id)

    if check:
        # Получаем кол-во выполненных заказов исполнителя
        count_performed_orders = await get_count_performed_orders_performer(user_id=user.id)

        # Получаем кол-во заказов в процессе модерации исполнителя
        count_moderate_orders = await get_count_moderate_orders(user_id=user.id)

        # Получаем кол-во заказов что ожидают выполнения исполнителя
        count_reserved_orders = await get_count_reserved_orders(user_id=user.id)

        text = "🛒 Мои заказы\n\n" \
               f"✅ Выполненные: {count_performed_orders} шт.\n" \
               f"⏳ В процессе модерации: {count_moderate_orders} шт.\n" \
               f"Ожидают выполнения: {count_reserved_orders} шт."

        markup = await performers_with_orders_kb(performed=count_performed_orders,
                                                 moderate=count_moderate_orders,
                                                 reserved=count_reserved_orders)

    else:
        text = "🛒 Мои заказы\n\n" \
               "🤷‍♂️ У вас нет заказов.\n\n" \
               "Хотите создать первый заказ?"

        markup = await performers_without_orders_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(NotBanned(), performers_with_orders_cd.filter(), state="*")
async def my_orders_performers_nav(call: types.CallbackQuery, user: Users,
                                   state: FSMContext, callback_data: dict = None, **kwargs):
    if callback_data:
        nav_btn = callback_data.get('nav_btn')
        await state.update_data(order_type=nav_btn)
    else:
        nav_btn = (await state.get_data()).get("order_type")

    if nav_btn == "performed":
        # Получаем кол-во выполненных заказов исполнителя
        count_performed_orders = await get_count_performed_orders_performer(user_id=user.id)

        # Получаем выполненные задания исполнителя
        orders = await get_performed_performers_orders(user_id=user.id)

        text = f"✅ Мои выполненные заказы: {count_performed_orders} шт.\n\n" \
               f"👇🏻 Узнать подробную информацию о заказе..."

        markup = await choose_performers_orders_kb(type_order='performed', orders=orders)

    elif nav_btn == "reserved":
        # Получаем кол-во заказов что ожидают выполнения исполнителя
        count_reserved_orders = await get_count_reserved_orders(user_id=user.id)

        # Получаем задания что ожидают выполнения исполнителя
        orders = await get_reserved_performers_orders(user_id=user.id)

        text = f"⏳ Мои заказы в процессе выполнения: {count_reserved_orders} шт.\n\n" \
               f"👇🏻 Узнать подробную информацию о заказе..."

        markup = await choose_performers_orders_kb(type_order='reserved', orders=orders)

    else:
        # Получаем кол-во заказов в процессе модерации исполнителя
        count_moderate_orders = await get_count_moderate_orders(user_id=user.id)

        # Получаем задания на модерации исполнителя
        orders = await get_moderate_performers_orders(user_id=user.id)

        text = f"⏳ Мои заказы в процессе модерации: {count_moderate_orders} шт.\n\n" \
               f"👇🏻 Узнать подробную информацию о заказе..."

        markup = await choose_performers_orders_kb(type_order='moderate', orders=orders)

    await call.message.edit_text(text=text, reply_markup=markup)


# Пагинатор для заданий
@dp.callback_query_handler(NotBanned(), paginator_performers_cd.filter(), state="*")
async def paginator_orders(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext):
    current_page = int(callback_data.get("page"))
    type_order = callback_data.get("type_order")

    if type_order == "performed":
        # Получаем выполненные задания исполнителя
        orders = await get_performed_performers_orders(user_id=user.id)

    elif type_order == "reserved":
        # Получаем задания что ожидают выполнения исполнителя
        orders = await get_reserved_performers_orders(user_id=user.id)

    else:
        # Получаем задания на модерации исполнителя
        orders = await get_moderate_performers_orders(user_id=user.id)

    markup = await choose_performers_orders_kb(type_order=type_order, orders=orders, page=current_page)
    await call.message.edit_reply_markup(reply_markup=markup)


# Выбранное задание
@dp.callback_query_handler(NotBanned(), choose_performers_orders_cd.filter(), state="*")
async def choose_performers_order(call: types.CallbackQuery, user: Users, state: FSMContext,
                                  callback_data: dict = None, **kwargs):

    if callback_data:
        order_id = int(callback_data.get("order"))
        type_order = callback_data.get("type_order")
        await state.update_data(order_id=order_id, type_order=type_order)

    else:
        data = await state.get_data()
        order_id = data.get("order_id")
        type_order = data.get("type_order")

    # Получение заказа по id
    order = await get_order_by_id(order_id=order_id)

    if order.type_order == "🔥":
        type_order_name = "🔥 Выкуп + отзыв + избранное"
        # Получение цены за услугу
        price = (await get_price_by_name(name="🔥")).price

    elif order.type_order == "💰":
        type_order_name = "💰 Выкуп"
        # Получение цены за услугу
        price = (await get_price_by_name(name="💰")).price

    else:
        type_order_name = "❤ Избранное"
        # Получение цены за услугу
        price = (await get_price_by_name(name="❤")).price

    if type_order == "performed":
        text = f"🔽🔽🔽 Заказ {order.order_name} 🔽🔽🔽\n\n" \
               f"Услуга - {type_order_name}\n\n" \
               f"Цена товара: {order.goods_cost} рублей\n" \
               f"🧮 Кэшбек/скидка: 196 рублей\n" \
               f"💳 Ваша награда: 2 балла + товар\n\n" \
               f"Название товара:\n{order.goods_name}\n\n" \
               f"Комментарии по заказу:\n{order.order_description}\n\n" \
               f"Ссылка на товар:\n{order.goods_link}\n\n" \
               f"Статус заказа: ✅ выполнен."

        markup = await choose_performers_order_kb()

    elif type_order == "reserved":
        text = f"🔽🔽🔽 Заказ {order.order_name} 🔽🔽🔽\n\n" \
               f"Услуга - {type_order_name}\n\n" \
               f"Цена товара: {order.goods_cost} рублей\n" \
               f"🧮 Кэшбек/скидка: 196 рублей\n" \
               f"💳 Ваша награда: 2 балла + товар\n\n" \
               f"Название товара:\n{order.goods_name}\n\n" \
               f"Комментарии по заказу:\n{order.order_description}\n\n" \
               f"Ссылка на товар:\n{order.goods_link}\n\n" \
               f"Статус заказа: ⏳ в процессе выполнения."

        markup = await choose_performers_reserved_order_kb(order_id=order.id, type_order=type_order,
                                                           order_link=order.goods_link)

    else:
        text = f"🔽🔽🔽 Заказ {order.order_name} 🔽🔽🔽\n\n" \
               f"Услуга - {type_order_name}\n\n" \
               f"Цена товара: {order.goods_cost} рублей\n" \
               f"🧮 Кэшбек/скидка: 196 рублей\n" \
               f"💳 Ваша награда: 2 балла + товар\n\n" \
               f"Название товара:\n{order.goods_name}\n\n" \
               f"Комментарии по заказу:\n{order.order_description}\n\n" \
               f"Ссылка на товар:\n{order.goods_link}\n\n" \
               f"Статус заказа: ⏳ в процессе модерации."

        markup = await choose_performers_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


# Кнопка выполнено на заказе
@dp.callback_query_handler(NotBanned(), chosen_performers_reserved_order_cd.filter(), state="*")
async def check_for_execution(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext):
    await state.set_state("check_for_execution")

    order_id = int(callback_data.get("order"))
    type_order = callback_data.get("type_order")

    photos = []

    await state.update_data(photos=photos)

    markup = await check_for_execution_kb(order_id=order_id, type_order=type_order)

    await call.message.edit_text(text="⏳ Пожалуйста, прикрепите скриншоты для подтверждения задания (до 5 шт), "
                                      "затем нажмите \"Готово\"\n\n"
                                      "👇🏻 Отправьте скриншоты только фото (не файлом!):",
                                 reply_markup=markup)


# Корректный тип
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.PHOTO, state="check_for_execution")
async def get_photo_check_for_execution(message: types.Message, user: Users, state: FSMContext, **kwargs):
    photos = (await state.get_data()).get("photos")

    if len(photos) < 5:
        photos.append(message.photo[-1].file_id)

    await state.update_data(photos=photos)


# Некорректный тип
@dp.message_handler(NotBanned(), content_types=types.ContentTypes.ANY, state="check_for_execution")
async def invalid_get_photo_check_for_execution(message: types.Message, user: Users, state: FSMContext, **kwargs):
    await message.delete()
    msg = await message.answer("Пожалуйста, прикрепите скриншоты для подтверждения задания (до 5 шт)\n\n"
                               "Отправьте скриншоты только фото (не файлом!)")
    await asyncio.sleep(5)
    await msg.delete()


# Кнопка ✅ Готово после ввода скриншотов
@dp.callback_query_handler(NotBanned(), check_for_execution_cd.filter(), state="*")
async def confirm_screenshots(call: types.CallbackQuery, callback_data: dict, user: Users, state: FSMContext):
    order_id = int(callback_data.get("order"))
    type_order = callback_data.get("type_order")

    # Получаем заказ
    order = await get_order_by_id(order_id)

    # Получаем заказчика задания
    customer = await get_user_by_id(user_id=order.user_id)

    performer = await get_user_by_telegram_id(call.message.chat.id)

    # Добавить заказ в модерацию
    moderate_order = await add_moderate_order(order_id=order_id, user_id=user.id)

    photos = (await state.get_data()).get("photos")

    media = types.MediaGroup()

    for photo in photos:
        media.attach_photo(photo)
        # Добавление медиа контента для задания которое проходит модерацию
        await add_media_content(moderate_order_id=moderate_order.id, file_id=photo)

    # Отправляем скриншоты админу
    await send_to_admins_media(media=media)

    # Отправляем выполненное задание админу
    await send_to_admins_performed_order(order=order, performer=user, customer=customer)

    notification_24h_job = scheduler.get_job(f"24h|{performer.id}-{order_id}")

    if notification_24h_job:
        notification_24h_job.remove()

    await call.message.delete()
    markup = await confirm_screenshots_kb()
    await call.message.answer(text="⏳ Ваше задание было отправлено на проверку, пожалуйста ожидайте.\n\n"
                                   "Проверка может занять до 3 дней.\n\n"
                                   "Отслеживать проверку вы можете в разделе \"На модерации\"",
                              reply_markup=markup)
