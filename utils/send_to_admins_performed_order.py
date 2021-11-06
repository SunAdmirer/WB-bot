from aiogram import types

from data.config import ADMINS
from loader import bot
from utils.db_api.models import Orders, Users


async def send_to_admins_performed_order(order: Orders, performer: Users, customer: Users):

    if order.type_order == "🔥":
        type_order_name = "🔥 Выкуп + отзыв + избранное"

    elif order.type_order == "💰":
        type_order_name = "💰 Выкуп"

    else:
        type_order_name = "❤ Избранное"

    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin,
                                   text="Внимание! Заказ выполнен\n\n"
                                        f"Исполнитель: {performer.id}|{performer.telegram_id}|{performer.username}\n"
                                        f"Заказчик: {customer.id}|{customer.telegram_id}|{customer.username}\n\n"
                                        f"Номер заказа(id): {order.id}\n"
                                        f"Тип заказа: {type_order_name}\n\n"
                                        f"Ссылка на товар: {order.goods_link}",
                                   disable_web_page_preview=True)

        except Exception as err:
            pass
