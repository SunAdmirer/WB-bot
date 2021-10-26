from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import notifications_cd, back_btn_cd


async def notifications_kb(btn: str, status: str) -> InlineKeyboardMarkup:

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
              InlineKeyboardButton(f"{btn}",
                                   callback_data=notifications_cd.new(
                                       status=status
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
