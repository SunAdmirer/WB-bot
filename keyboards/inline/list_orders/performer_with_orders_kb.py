from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import back_btn_cd, list_orders_cd


async def performer_with_orders_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("🔥 Выкуп + отзыв + ❤",
                                     callback_data=list_orders_cd.new(
                                         nav_btn="🔥",
                                         order_id='-'
                                     ))
            ],
            [
                InlineKeyboardButton("💰 Выкуп",
                                     callback_data=list_orders_cd.new(
                                         nav_btn="💰",
                                         order_id='-'
                                     ))
            ],
            [
                InlineKeyboardButton("❤ Избранное",
                                     callback_data=list_orders_cd.new(
                                         nav_btn="❤",
                                         order_id='-'
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
