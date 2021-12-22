from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import back_btn_cd, list_orders_cd


async def show_order_kb(type_order: str, url: str, order_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔗 Ссылка",
                                     url=url)
            ],
            [
                InlineKeyboardButton("☑️ Выполнить",
                                     callback_data=list_orders_cd.new(
                                         nav_btn="execute",
                                         order_id=order_id
                                     ))
            ],
            [
                InlineKeyboardButton("Пропустить",
                                     callback_data=list_orders_cd.new(
                                         nav_btn=type_order,
                                         order_id='-'
                                     ))
            ],
            [
                InlineKeyboardButton("◀ Назад",
                                     callback_data=back_btn_cd.new(
                                         nav_btn="list_orders_menu"
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
