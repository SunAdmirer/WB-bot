import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import NotBanned
from keyboards.inline.balance.withdrawal_kb import show_withdrawal_form_keyboard, next_step_withdrawal_kb
from loader import dp
from utils.db_api.models import Users


@dp.callback_query_handler(NotBanned(), text="withdrawal", state="*")
async def withdrawal_balance(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    text = "<b>🤑 Вывод средств</b>\n\n" \
           f"<b>Ваш id:</b> {user.telegram_id}\n" \
           f"<b>Вам доступно для вывода:</b> {user.balance} руб.\n\n" \
           f"*вывод средств от 500 руб.*\n\n" \
           f"👇🏻 Вывести средства:"

    markup = await show_withdrawal_form_keyboard()

    await call.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(NotBanned(), text="next_step_withdrawal", state="*")
async def next_step_withdrawal(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    if user and user.balance >= 500.00:
        markup = await next_step_withdrawal_kb()

        await call.message.edit_text(f"<b>🤑 Вывод средств</b>\n\n"
                                     f"<b>Твой id:</b> {user.telegram_id}\n\n"
                                     f"Что бы вывести средства, напиши админу @vasilyiusi и "
                                     f"не забудь указать свой id и сумму на вывод.")
        await call.message.edit_reply_markup(markup)
    else:
        error_msg = await call.message.answer("❗️Вывод средств доступен только от 500 руб.")
        await asyncio.sleep(4)
        await error_msg.delete()
