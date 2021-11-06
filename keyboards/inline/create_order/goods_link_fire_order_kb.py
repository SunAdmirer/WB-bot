from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import back_btn_cd


async def goods_link_fire_order_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("◀ Назад",
                                     callback_data=back_btn_cd.new(
                                         nav_btn="cashback_fire_order"
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
