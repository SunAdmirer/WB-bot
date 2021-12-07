from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsGroups
from keyboards.inline.callback_datas import admins_confirmed_cd
from loader import dp
from utils.db_api.commands.orders_cmds import get_order_by_id, update_moderate_order_confirmed, \
    get_moderate_performers_order, get_media_content

from utils.db_api.commands.users_cmds import get_user_by_id
from utils.send_to_customers_media import send_to_customers_media
from utils.send_to_customers_performed_order import send_to_customers_performed_order


# Подтверждение/Отклонение выполнения заказа
@dp.callback_query_handler(IsGroups(), admins_confirmed_cd.filter(confirm_type='performed_confirm'), state="*")
async def admins_performed_confirm_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext, **kwargs):
    nav_btn = callback_data.get('nav_btn')
    performer_id = int(callback_data.get('performer_id'))
    order_id = int(callback_data.get('order_id'))

    if nav_btn == 'confirm':
        # Достаем заказ
        order = await get_order_by_id(order_id)

        # Достаем задание на модерации исполнителя
        moderate_order = await get_moderate_performers_order(performer_id=performer_id, order_id=order_id)

        # Достаем фото для заказа в модерации исполнителя
        media_content = await get_media_content(moderate_order_id=moderate_order.id)

        media = types.MediaGroup()

        for content in media_content:
            media.attach_photo(content.file_id)

        # Достаем заказчика
        customer = await get_user_by_id(user_id=order.user_id)

        # Админ подтверждает выполнение
        await update_moderate_order_confirmed(order_id=order_id, confirmed=True)

        # Отправляем скриншоты заказчику
        await send_to_customers_media(media=media, customer=customer)

        # Отправляем выполненное задание заказчику
        await send_to_customers_performed_order(order=order, customer=customer)

        await call.message.edit_text(f"✅  Выполнение заказа({order_id} одобренно!)",
                                     reply_markup=None)

    elif nav_btn == 'reject':
        await call.message.edit_text(f"❌ Выполнение заказа({order_id}) отклонено!",
                                     reply_markup=None)
