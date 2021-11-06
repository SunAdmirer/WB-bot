from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import main_menu_cd, back_btn_cd, balance_menu_cd
from utils.db_api.commands.orders_cmds import get_unpaid_orders
from utils.db_api.models import Users


async def balance_menu_kb(user: Users) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    # Получаем все неоплаченные заказы пользователя
    unpaid_orders = await get_unpaid_orders(user_id=user.id)

    markup.insert(
        InlineKeyboardButton(text="➕ Создать заказ",
                             callback_data=main_menu_cd.new(
                                 nav_btn="create_order"
                             ))
    )

    for unpaid_order in unpaid_orders:
        markup.insert(
            InlineKeyboardButton(text=f"ЗАКАЗ {unpaid_order.order_name}",
                                 callback_data=balance_menu_cd.new(
                                     order_id=unpaid_order.id
                                 ))
        )

    markup.insert(
        InlineKeyboardButton(text="Вывод средств",
                             callback_data="withdrawal")
    )

    markup.insert(
        InlineKeyboardButton("📁 Главное меню",
                             callback_data=back_btn_cd.new(
                                 nav_btn="main_menu"
                             ))
    )

    return markup
