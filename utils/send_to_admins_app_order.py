from aiogram import types

from data.config import ADMINS_GROUP
from keyboards.inline.send_to_admins_kb import send_to_admins_app_order_kb
from loader import bot
from utils.db_api.models import Orders, Users


# Заявка на бронирование заказа в чат админов
async def send_to_admins_app_order(order: Orders, performer: Users):

    if order.type_order == "🔥":
        type_order_name = "🔥 Выкуп + отзыв + избранное"

    elif order.type_order == "💰":
        type_order_name = "💰 Выкуп"

    else:
        type_order_name = "❤ Избранное"

    markup = await send_to_admins_app_order_kb(username=performer.username,
                                               performer_id=performer.id,
                                               order_id=order.id)

    users_mention = f"<a href=\"tg://user?id={performer.telegram_id}\">{performer.username}</a>"

    try:
        await bot.send_message(chat_id=ADMINS_GROUP,
                               text="Внимание! Заявка на бронирование заказа\n\n"
                                    f"Исполнитель {users_mention}: "
                                    f"{performer.id}|{performer.telegram_id}|{performer.username}\n\n"
                                    f"Номер заказа(id): {order.id}\n"
                                    f"Тип заказа: {type_order_name}\n\n"
                                    f"Ссылка на товар: {order.goods_link}",
                               reply_markup=markup,
                               disable_web_page_preview=True)

    except Exception as err:
        print(err)
