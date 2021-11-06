from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import back_btn_cd, confirm_favorites_order_cd


async def confirm_favorites_order_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Заказать ✅",
                                     callback_data=confirm_favorites_order_cd.new(
                                         nav_btn="confirm"
                                     ))
            ],
            [
                InlineKeyboardButton("◀ Назад",
                                     callback_data=back_btn_cd.new(
                                         nav_btn="contacts_favorites_order"
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
