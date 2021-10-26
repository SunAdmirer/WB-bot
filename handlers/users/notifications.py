from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import NotBanned
from keyboards.inline.callback_datas import notifications_cd
from keyboards.inline.notifications_kb import notifications_kb
from loader import dp
from utils.db_api.commands.users_cmds import get_user_by_telegram_id, update_notification_user
from utils.db_api.models import Users


async def notifications(call: CallbackQuery, **kwargs):
    user = await get_user_by_telegram_id(call.message.chat.id)

    # Проверка включены ли уведомления у пользователя
    if user.notifications:
        btn = "🔕 Выкл. уведомления"
        text = "🔔 Уведомления о заказах <b>включены.</b>\n\n" \
               "👇🏻 Выключить уведомления:"
        status = "off"
    else:
        btn = "🔔 Вкл. уведомления"
        text = "🔕 Уведомления о заказах <b>выключены.</b>\n\n" \
               "👇🏻 Включить уведомления:"
        status = "on"

    markup = await notifications_kb(btn, status)

    await call.message.edit_text(text)
    await call.message.edit_reply_markup(markup)


@dp.callback_query_handler(NotBanned(), notifications_cd.filter(), state="*")
async def notifications_switch(call: CallbackQuery, user: Users, callback_data: dict, state: FSMContext):
    status = callback_data.get("status")

    text = ''
    btn = ''

    if status == "off":
        btn = "🔔 Вкл. уведомления"
        text = "🔕 Уведомления о заказах <b>выключены.</b>\n\n" \
               "👇🏻 Включить уведомления:"
        status = "on"

        # Выключаем уведомления
        await update_notification_user(call.message.chat.id, False)

    elif status == "on":
        btn = "🔕 Выкл. уведомления"
        text = "🔔 Уведомления о заказах <b>включены.</b>\n\n" \
               "👇🏻 Выключить уведомления:"
        status = "off"

        # Включаем уведомления
        await update_notification_user(call.message.chat.id, True)

    markup = await notifications_kb(btn, status)

    await call.message.edit_text(text)
    await call.message.edit_reply_markup(markup)
