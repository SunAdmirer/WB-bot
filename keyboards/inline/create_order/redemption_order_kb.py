from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import redemption_order_cd, back_btn_cd


# Выбор кол-во выполнений
async def redemption_order_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("💰 10",
                                     callback_data=redemption_order_cd.new(
                                         nav_btn="10"
                                     ))
            ],
            [
                InlineKeyboardButton("💰 30",
                                     callback_data=redemption_order_cd.new(
                                         nav_btn="30"
                                     ))
            ],
            [
                InlineKeyboardButton("💰 50",
                                     callback_data=redemption_order_cd.new(
                                         nav_btn="50"
                                     ))
            ],
            [
                InlineKeyboardButton("💰 100",
                                     callback_data=redemption_order_cd.new(
                                         nav_btn="100"
                                     ))
            ],
            [
                InlineKeyboardButton("◀ Назад",
                                     callback_data=back_btn_cd.new(
                                         nav_btn="create_order_menu"
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
