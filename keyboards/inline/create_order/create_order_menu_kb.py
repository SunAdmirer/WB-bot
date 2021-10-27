from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import back_btn_cd, create_order_menu_cd


# Кнопки для меню создания заказа
async def create_order_menu_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("🔥 Выкуп + отзыв + ❤",
                                     callback_data=create_order_menu_cd.new(
                                         nav_btn="🔥"
                                     ))
            ],
            [
                InlineKeyboardButton("💰 Выкуп",
                                     callback_data=create_order_menu_cd.new(
                                         nav_btn="💰"
                                     ))
            ],
            [
                InlineKeyboardButton("❤ Избранное",
                                     callback_data=create_order_menu_cd.new(
                                         nav_btn="❤"
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
