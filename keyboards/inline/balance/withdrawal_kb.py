from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import back_btn_cd


async def show_withdrawal_form_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("💳 Вывести",
                                     callback_data='next_step_withdrawal')
            ],
            [
                InlineKeyboardButton("◀ Назад",
                                     callback_data=back_btn_cd.new(
                                         nav_btn="balance_menu"
                                     ))
            ],
            [
                InlineKeyboardButton("📁 Главное меню",
                                     callback_data="back_to_main_menu")
            ]
        ]
    )

    return markup


async def next_step_withdrawal_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("◀ Назад",
                                     callback_data=back_btn_cd.new(
                                         nav_btn="withdrawal_balance"
                                     ))
            ],
            [
                InlineKeyboardButton("📁 Главное меню",
                                     callback_data="back_to_main_menu")
            ]
        ]
    )

    return markup
