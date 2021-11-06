import math
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import choose_performers_orders_cd, paginator_performers_cd, back_btn_cd
from utils.db_api.commands.orders_cmds import get_order_by_id
from utils.db_api.models import Orders


async def choose_performers_orders_kb(type_order: str, orders: List[Orders], page: int = 1) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    MAX_PER_PAGE = 5
    first_index = (page - 1) * MAX_PER_PAGE
    last_index = page * MAX_PER_PAGE

    sliced_array = orders[first_index:last_index]

    if type_order == "performed":
        emoji_order = "✅"
    else:
        emoji_order = "⏳"

    for order in sliced_array:
        order_ = await get_order_by_id(order.order_id)
        markup.insert(InlineKeyboardButton(f"{emoji_order} Заказ {order_.order_name}",
                                           callback_data=choose_performers_orders_cd.new(
                                               order=f"{order_.id}",
                                               type_order=type_order
                                           )))

    total_pages = math.ceil(len(orders) / 5)

    if total_pages == 1:
        pass

    # Стр. << 2/3 >>
    elif total_pages > page > 1:
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton("⬅",
                                     callback_data=paginator_performers_cd.new(type_order=type_order, page=page - 1)),
                InlineKeyboardButton(f"Стр. {page}/{total_pages}",
                                     callback_data=paginator_performers_cd.new(type_order=type_order,
                                                                               page="current_page")),
                InlineKeyboardButton("➡",
                                     callback_data=paginator_performers_cd.new(type_order=type_order, page=page + 1)),
            ]
        )

    # Стр. 1/3 >>
    elif page == 1:
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton(" ",
                                     callback_data=paginator_performers_cd.new(type_order=type_order, page=page)),
                InlineKeyboardButton(f"Стр. {page}/{total_pages}",
                                     callback_data=paginator_performers_cd.new(type_order=type_order,
                                                                               page="current_page")),
                InlineKeyboardButton("➡",
                                     callback_data=paginator_performers_cd.new(type_order=type_order, page=page + 1)),
            ]
        )

    # Стр. << 3/3
    elif page == total_pages:
        markup.inline_keyboard.append(
            [
                InlineKeyboardButton("⬅",
                                     callback_data=paginator_performers_cd.new(type_order=type_order, page=page - 1)),
                InlineKeyboardButton(f"Стр. {page}/{total_pages}",
                                     callback_data=paginator_performers_cd.new(type_order=type_order,
                                                                               page="current_page")),
                InlineKeyboardButton(" ",
                                     callback_data=paginator_performers_cd.new(type_order=type_order, page=page)),
            ]
        )

    markup.insert(
        InlineKeyboardButton("◀ Назад",
                             callback_data=back_btn_cd.new(
                                 nav_btn="my_orders_performers"
                             ))
    )

    markup.insert(
        InlineKeyboardButton("📁 Главное меню",
                             callback_data=back_btn_cd.new(
                                 nav_btn="main_menu"
                             ))
    )

    return markup
