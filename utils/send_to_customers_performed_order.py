from keyboards.inline.customers_performed_orders_kb import send_to_customers_performed_order_kb
from loader import bot
from utils.db_api.models import Orders, Users


async def send_to_customers_performed_order(order: Orders, customer: Users):
    if order.type_order == "🔥":
        type_order_name = "🔥 Выкуп + отзыв + избранное"

    elif order.type_order == "💰":
        type_order_name = "💰 Выкуп"

    else:
        type_order_name = "❤ Избранное"

    markup = await send_to_customers_performed_order_kb(order_id=order.id, customer_id=customer.id)

    try:
        await bot.send_message(chat_id=customer.telegram_id,
                               text=f"Внимание!\n\n"
                                    f"Пользователь выполнил ваше задание {order.order_name}\n\n"
                                    f"Услуга:\n{type_order_name}\n\n"
                                    f"Ссылка на товар:\n{order.goods_link}\n\n"
                                    f"Скриншоты выполнения прилагаются к сообщению.\n\n"
                                    f"Внимательно проверьте выполнение задания и затем "
                                    f"подтвердите его. Отменить действие будет нельзя!\n\n"
                                    f"При отсутствии подтверждения в течение 3 дней, "
                                    f"задание подтверждается автоматически.\n\n"
                                    f"Подтверждаете?",
                               reply_markup=markup)

    except Exception as err:
        pass
