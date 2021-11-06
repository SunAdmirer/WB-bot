from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import back_btn_cd, chosen_performers_reserved_order_cd


async def choose_performers_reserved_order_kb(order_id: int, type_order: str, order_link: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ссылка на товар",
                                     url=order_link)
            ],
            [
                InlineKeyboardButton(text="✅ Выполнено",
                                     callback_data=chosen_performers_reserved_order_cd.new(
                                         order=order_id,
                                         type_order=type_order,
                                     ))
            ],
            [
                InlineKeyboardButton("◀ Назад",
                                     callback_data=back_btn_cd.new(
                                         nav_btn="my_orders_performers_nav"
                                     ))
            ],
            [
                InlineKeyboardButton("📁 Главное меню",
                                     callback_data=back_btn_cd.new(
                                         nav_btn="main_menu"
                                     ))
            ]
        ]
    )

    return markup
