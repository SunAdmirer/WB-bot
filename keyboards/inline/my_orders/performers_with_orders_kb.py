from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import back_btn_cd, performers_with_orders_cd


async def performers_with_orders_kb(performed: int, moderate: int, reserved: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    if performed != 0:
        markup.insert(
            InlineKeyboardButton(text="✅ Выполненные",
                                 callback_data=performers_with_orders_cd.new(
                                     nav_btn="performed"
                                 ))
        )

    if reserved != 0:
        markup.insert(
            InlineKeyboardButton(text="Ожидают выполнения",
                                 callback_data=performers_with_orders_cd.new(
                                     nav_btn="reserved"
                                 ))
        )

    if moderate != 0:
        markup.insert(
            InlineKeyboardButton(text="⏳ Модерация",
                                 callback_data=performers_with_orders_cd.new(
                                     nav_btn="moderate"
                                 ))
        )

    markup.insert(
        InlineKeyboardButton("📁 Главное меню",
                             callback_data=back_btn_cd.new(
                                 nav_btn="main_menu"
                             ))
    )

    return markup
