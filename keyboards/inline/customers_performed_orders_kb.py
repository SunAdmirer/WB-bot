from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import customers_confirmed_cd


async def send_to_customers_performed_order_kb(order_id: int, customer_id: int,
                                               performer_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("✅ Подтвердить",
                                     callback_data=customers_confirmed_cd.new(
                                         confirm_type="customer_performed",
                                         customer_id=customer_id,
                                         performer_id=performer_id,
                                         order_id=order_id,
                                         nav_btn='confirm'
                                     ))
            ],
            [
                InlineKeyboardButton("❌ Отклонить",
                                     callback_data=customers_confirmed_cd.new(
                                         confirm_type="customer_performed",
                                         customer_id=customer_id,
                                         performer_id=performer_id,
                                         order_id=order_id,
                                         nav_btn='reject'
                                     ))
            ]
        ]
    )

    return markup


async def customers_confirmed_order_kb(order_id: int, customer_id: int,
                                       confirm_type: str, performer_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Да",
                                     callback_data=customers_confirmed_cd.new(
                                         confirm_type=confirm_type,
                                         customer_id=customer_id,
                                         performer_id=performer_id,
                                         order_id=order_id,
                                         nav_btn='yes'
                                     ))
            ],
            [
                InlineKeyboardButton("Нет",
                                     callback_data=customers_confirmed_cd.new(
                                         confirm_type=confirm_type,
                                         customer_id=customer_id,
                                         performer_id=performer_id,
                                         order_id=order_id,
                                         nav_btn='no'
                                     ))
            ]
        ]
    )

    return markup
