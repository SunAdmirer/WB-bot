from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import back_btn_cd, customers_with_orders_cd


async def customers_with_orders_kb(performed: int, in_process: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    if performed != 0:
        markup.insert(
            InlineKeyboardButton(text="✅ Выполненные",
                                 callback_data=customers_with_orders_cd.new(
                                     nav_btn="performed"
                                 ))
        )

    if in_process != 0:
        markup.insert(
            InlineKeyboardButton(text="⏳ В процессе выполнения",
                                 callback_data=customers_with_orders_cd.new(
                                     nav_btn="in_process"
                                 ))
        )

    markup.insert(
        InlineKeyboardButton("📁 Главное меню",
                             callback_data=back_btn_cd.new(
                                 nav_btn="main_menu"
                             ))
    )

    return markup
