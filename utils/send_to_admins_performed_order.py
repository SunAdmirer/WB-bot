from aiogram import types

from data.config import ADMINS_GROUP
from keyboards.inline.send_to_admins_kb import send_to_admins_performed_order_kb
from loader import bot
from utils.db_api.models import Orders, Users


async def send_to_admins_performed_order(order: Orders, performer: Users, customer: Users):

    if order.type_order == "🔥":
        type_order_name = "🔥 Выкуп + отзыв + избранное"

    elif order.type_order == "💰":
        type_order_name = "💰 Выкуп"

    else:
        type_order_name = "❤ Избранное"

    performer_mention = f"<a href=\"tg://user?id={performer.telegram_id}\">{performer.username}</a>"
    customer_mention = f"<a href=\"tg://user?id={customer.telegram_id}\">{customer.username}</a>"

    markup = await send_to_admins_performed_order_kb(username=performer.username,
                                                     performer_id=performer.id,
                                                     order_id=order.id)

    try:
        await bot.send_message(chat_id=ADMINS_GROUP,
                               text="Внимание! Заказ выполнен\n\n"
                                    f"Исполнитель {performer_mention}: "
                                    f"{performer.id}|{performer.telegram_id}|{performer.username}\n"
                                    f"Заказчик {customer_mention}: "
                                    f"{customer.id}|{customer.telegram_id}|{customer.username}\n\n"
                                    f"Номер заказа(id): {order.id}\n"
                                    f"Тип заказа: {type_order_name}\n\n"
                                    f"Ссылка на товар: {order.goods_link}",
                               reply_markup=markup,
                               disable_web_page_preview=True)

    except Exception as err:
        pass
