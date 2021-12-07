from data.config import ADMINS_GROUP
from loader import bot
from utils.db_api.commands.orders_cmds import get_reserved_order_to_user, get_order_by_id
from utils.db_api.commands.users_cmds import get_user_by_id


async def notification_one_day_after_take_order(reserved_order_id: int):
    reserved_order = await get_reserved_order_to_user(reserved_order_id)
    order = await get_order_by_id(reserved_order.order_id)

    performer = await get_user_by_id(reserved_order.user_id)
    customer = await get_order_by_id(order.user_id)

    performer_mention = f"<a href=\"tg://user?id={performer.telegram_id}\">{performer.username}</a>"
    customer_mention = f"<a href=\"tg://user?id={customer.telegram_id}\">{customer.username}</a>"

    if order.type_order == "🔥":
        type_order_name = "🔥 Выкуп + отзыв + избранное"

    elif order.type_order == "💰":
        type_order_name = "💰 Выкуп"

    else:
        type_order_name = "❤ Избранное"

    try:
        await bot.send_message(chat_id=ADMINS_GROUP,
                               text="Внимание! Прошло 24 часа после того, "
                                    "как исполнитель взял заказ, но так и не выполнил его\n\n"
                                    f"Исполнитель {performer_mention}: "
                                    f"{performer.id}|{performer.telegram_id}|{performer.username}\n"
                                    f"Заказчик {customer_mention}: "
                                    f"{customer.id}|{customer.telegram_id}|{customer.username}\n\n"
                                    f"Номер заказа(id): {order.id}\n"
                                    f"Тип заказа: {type_order_name}\n\n"
                                    f"Ссылка на товар: {order.goods_link}",
                               disable_web_page_preview=True)

    except Exception as err:
        pass
