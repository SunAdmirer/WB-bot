from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import LabeledPrice

from filters import NotBanned
from keyboards.inline.balance.balance_menu_kb import balance_menu_kb
from keyboards.inline.balance.paid_for_order_kb import paid_for_order_kb
from keyboards.inline.balance.process_successful_payment_kb import process_successful_payment_kb
from keyboards.inline.callback_datas import balance_menu_cd
from loader import dp, bot
from utils.db_api.commands.orders_cmds import get_order_by_id, update_order_paid_for_by_id
from utils.db_api.commands.price_list_cmds import get_price_by_name
from utils.db_api.commands.referrals_cmds import get_recruiter, change_bonus_false
from utils.db_api.commands.transaction_cmds import add_translation
from utils.db_api.commands.users_cmds import increase_user_balance, get_user_by_id, increase_user_balance_from_ref
from utils.db_api.models import Users, Referrals

from utils.misc.payments_telegram import Payment


async def balance_menu(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    text = f"<b>💵 Ваш баланс:</b> {user.balance} руб.\n" \
           f"<b>👤 Ваш id:</b> {user.telegram_id}\n\n" \
           f"👇🏻 Чтобы пополнить баланс, сначала создайте заказ. Если заказ создан, выберите его ниже:"

    markup = await balance_menu_kb(user=user)

    await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(NotBanned(), balance_menu_cd.filter(), state="*")
async def paid_for_order(call: types.CallbackQuery, user: Users, state: FSMContext,
                         callback_data: dict = None, **kwargs):
    if callback_data:
        order_id = int(callback_data.get('order_id'))
        await state.update_data(current_order_id=order_id)
    else:
        order_id = int((await state.get_data()).get("current_order_id"))

    # Получение заказа по id
    order = await get_order_by_id(order_id=order_id)

    if order.type_order == "🔥":
        type_order_name = "🔥 Выкуп + отзыв + избранное"

    elif order.type_order == "💰":
        type_order_name = "💰 Выкуп"

    else:
        type_order_name = "❤ Избранное"

    text = f"Название товара: {order.goods_name}\n\n" \
           f"Услуга: {type_order_name}\n" \
           f"Количество участников: {order.goal_amount}\n" \
           f"Размер кешбэка/скидки: {order.cashback} рублей\n\n" \
           f"Сумма для пополнения: {order.order_cost} рублей\n\n" \
           f"👇Нажмите на кнопку ниже, чтобы продолжить пополнение баланса"

    markup = await paid_for_order_kb()

    await call.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(NotBanned(), text="pay_for_order", state="*")
async def send_invoice(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    order_id = int((await state.get_data()).get("current_order_id"))

    # Получение заказа по id
    order = await get_order_by_id(order_id=order_id)

    amount = int(str(int(order.order_cost)) + "_00")

    payment = Payment(
        title="Marketplace cashback Bot",
        description="Пополнение на:",
        start_parameter="",
        currency='RUB',
        prices=[
            LabeledPrice(label="Пополнение баланса",
                         amount=amount)
        ]
    )

    await bot.send_invoice(chat_id=call.message.chat.id,
                           **payment.generate_invoice(),
                           payload=f"{user.id}|{user.telegram_id}|{order.id}")


@dp.pre_checkout_query_handler(state="*")
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print("\nprocess_pre_checkout_query\n")
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)


@dp.message_handler(state="*", content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message, user: Users, **kwargs):
    print("\nprocess_successful_payment\n")
    successful_payment = message.successful_payment

    order_id = int(successful_payment.invoice_payload.split('|')[2])
    amount = successful_payment.total_amount / 100

    # Получение заказа по id
    order = await get_order_by_id(order_id=order_id)

    # Добавление транзакции
    await add_translation(user_id=user.id, amount=amount)

    # Увеличить баланс пользователя
    await increase_user_balance(user_id=user.id, amount=amount)

    # Обновляем paid_for заказа
    await update_order_paid_for_by_id(order_id=order.id, paid_for=True)

    # Узнаем кто привел пользователя
    referrals: Referrals = await get_recruiter(recruit_id=user.id)

    # Если пользователя привел человек и если бонус еще не был активирован
    if referrals and referrals.bonus:
        # Получаем рекрутера (Того кто привел нового пользователя)
        recruiter = await get_user_by_id(user_id=referrals.recruiter_id)

        recruiter_bonus = (await get_price_by_name(name="recruiter_bonus")).price
        recruit_bonus = (await get_price_by_name(name="recruit_bonus")).price

        # Считаем бонус рекруту
        recruit_bonus_ = float(amount) * float(recruit_bonus) / 100
        # Начисляем бонус рекруту
        await increase_user_balance(user_id=user.id, amount=recruit_bonus_)

        # Считаем бонус рекрутеру
        recruiter_bonus_ = float(amount) * float(recruiter_bonus) / 100
        # Начисляем бонус рекрутеру
        await increase_user_balance(user_id=recruiter.id, amount=recruiter_bonus_)

        # Увеличить баланс с реф. программы Рекрутеру
        await increase_user_balance_from_ref(user_id=recruiter.id, amount=amount)

        # забирем бонус
        await change_bonus_false(referrals.id)

    text = f"👌 Операция прошла успешно!\n\n" \
           f"Ваш заказ: {order.order_name}\n" \
           f"Вы можете следить за заказом перейдя в \"🛒 Мои заказы\"\n\n" \
           f"💰 Ваш баланс не будет списываться, пока вы не подтвердите выполнение задания."

    markup = await process_successful_payment_kb()

    await message.answer(text=text, reply_markup=markup)
