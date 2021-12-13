from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import admins_confirmed_cd


# Подтверждение/Отклонение заявки на бронирование заказа
async def send_to_admins_app_order_kb(username: str, performer_id: int,
                                      order_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Одобрить",
                                     callback_data=admins_confirmed_cd.new(
                                         confirm_type='app_confirm',
                                         performer_id=performer_id,
                                         order_id=order_id,
                                         nav_btn='confirm'
                                     ))
            ],
            [
                InlineKeyboardButton(text="Отклонить",
                                     callback_data=admins_confirmed_cd.new(
                                         confirm_type='app_confirm',
                                         performer_id=performer_id,
                                         order_id=order_id,
                                         nav_btn='reject'
                                     ))
            ]
        ]
    )

    if username != "Without a username":
        markup.insert(
            InlineKeyboardButton(text="Написать пользователю",
                                 url=f'https://t.me/{username}')
        )

    return markup


# Подтверждение/Отклонение выполнения заказа
async def send_to_admins_performed_order_kb(username: str, performer_id: int,
                                            customer_id: int, order_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Одобрить",
                                     callback_data=admins_confirmed_cd.new(
                                         confirm_type='performed_confirm',
                                         performer_id=performer_id,
                                         customer_id=customer_id,
                                         order_id=order_id,
                                         nav_btn='confirm'
                                     ))
            ],
            [
                InlineKeyboardButton(text="Отклонить",
                                     callback_data=admins_confirmed_cd.new(
                                         confirm_type='performed_confirm',
                                         performer_id=performer_id,
                                         customer_id=customer_id,
                                         order_id=order_id,
                                         nav_btn='reject'
                                     ))
            ]
        ]
    )

    if username != "Without a username":
        markup.insert(
            InlineKeyboardButton(text="Написать пользователю",
                                 url=f'https://t.me/{username}')
        )

    return markup


# Двойное Подтверждение/Отклонение выполнения заказа
async def admins_performed_confirm_order_kb(performer_id: int,
                                            customer_id: int, order_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да",
                                     callback_data=admins_confirmed_cd.new(
                                         confirm_type='performed_confirm2',
                                         performer_id=performer_id,
                                         customer_id=customer_id,
                                         order_id=order_id,
                                         nav_btn='confirm'
                                     ))
            ],
            [
                InlineKeyboardButton(text="Нет",
                                     callback_data=admins_confirmed_cd.new(
                                         confirm_type='performed_confirm2',
                                         performer_id=performer_id,
                                         customer_id=customer_id,
                                         order_id=order_id,
                                         nav_btn='reject'
                                     ))
            ]
        ]
    )

    return markup


# Кнопка назад после двойного отклонения заказа
async def reject_double_confirmed(performer_id: int,
                                  customer_id: int, order_id: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад",
                                     callback_data=admins_confirmed_cd.new(
                                         confirm_type='performed_confirm',
                                         performer_id=performer_id,
                                         customer_id=customer_id,
                                         order_id=order_id,
                                         nav_btn='reject'
                                     ))
            ]
        ]
    )

    return markup
