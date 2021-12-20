from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import SUPPORT_LINK
from keyboards.inline.callback_datas import main_menu_cd


# Клавиатура для главного меню
async def main_menu_kb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Создать заказ",
                                     callback_data=main_menu_cd.new(
                                         nav_btn="create_order"
                                     ))
            ],
            [
                InlineKeyboardButton(text="💰 Биржа заданий",
                                     callback_data=main_menu_cd.new(
                                         nav_btn="list_orders"
                                     ))
            ],
            [
                InlineKeyboardButton(text="💸 Партнерский заработок",
                                     callback_data=main_menu_cd.new(
                                         nav_btn="referrals"
                                     ))
            ],
            [
                InlineKeyboardButton(text="💬 Поддержка",
                                     url=SUPPORT_LINK),
                InlineKeyboardButton(text="💵 Баланс",
                                     callback_data=main_menu_cd.new(
                                         nav_btn="balance"
                                     )),
            ],
            [
                InlineKeyboardButton(text="🛒 Мои заказы",
                                     callback_data=main_menu_cd.new(
                                         nav_btn="my_orders"
                                     )),
                InlineKeyboardButton(text="🔔 Уведомления",
                                     callback_data=main_menu_cd.new(
                                         nav_btn="notifications"
                                     )),
            ],
            [
                InlineKeyboardButton(text="📢 Пригласить друзей", switch_inline_query='')
            ]
        ]
    )

    return markup
