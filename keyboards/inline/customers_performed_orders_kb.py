from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import customers_confirmed_cd


async def send_to_customers_performed_order_kb(order_id: int, customer_id: int,
                                               performer_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("✅ Подтвердить",
                                     callback_data=customers_confirmed_cd.new(
                                         confirm_type="confirm",
                                         customer_id=customer_id,
                                         performer_id=performer_id,
                                         order_id=order_id
                                     ))
            ],
            [
                InlineKeyboardButton("❌ Отклонить",
                                     callback_data=customers_confirmed_cd.new(
                                         confirm_type="reject",
                                         customer_id=customer_id,
                                         performer_id=performer_id,
                                         order_id=order_id
                                     ))
            ]
        ]
    )

    return markup


async def customers_confirmed_order_kb(order_id: int, customer_id: int,
                                       performer_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Да",
                                     callback_data=customers_confirmed_cd.new(
                                         confirm_type="confirm2",
                                         customer_id=customer_id,
                                         performer_id=performer_id,
                                         order_id=order_id
                                     ))
            ],
            [
                InlineKeyboardButton("Нет",
                                     callback_data=customers_confirmed_cd.new(
                                         confirm_type="reject2",
                                         customer_id=customer_id,
                                         performer_id=performer_id,
                                         order_id=order_id
                                     ))
            ]
        ]
    )

    return markup
