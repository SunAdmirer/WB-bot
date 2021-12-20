from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.referrals_kb import referrals_kb
from loader import bot
from utils.db_api.commands.users_cmds import count_recruit, get_user_by_telegram_id, get_balance_from_ref
from utils.db_api.models import Users


async def referrals(call: types.CallbackQuery, user: Users, state: FSMContext, **kwargs):
    bot_username = (await bot.me).username

    recruiter = await get_user_by_telegram_id(call.message.chat.id)
    balance_from_ref = await get_balance_from_ref(recruiter.id)

    count_recruit_ = await count_recruit(recruiter_id=recruiter.id)

    text = "💰 Партнёрская программа\n\n" \
           "Привлекайте активных друзей и получайте до 50 000₽ в месяц.\n\n" \
           "1. Вы рекламируете вашу партнерскую ссылку:\n\n" \
           f"https://t.me/{bot_username}?start={call.message.chat.id}\n" \
           f"Или нажмите 📢 Пригласить друзей.\n" \
           f"2. К примеру, по ссылке выше перешло 10 человек в биржу и пополнили" \
           f" баланс на сумму 5000₽, ваша прибыль получится 1000₽ (дарим 20% прибыли)\n" \
           f"3. Итого, рекомендуя биржу, вы заработаете до 50.000₽ в первый месяц!\n\n" \
           f"💵 +20.00% на баланс от пополнения по вашей реферальной ссылке.\n" \
           f"💵 +10.00% бонус приглашенному другу.\n\n" \
           f"Всего рефералов: {count_recruit_}\n" \
           f"Всего заработано от рефералов: {round(balance_from_ref, 2)} руб."

    markup = await referrals_kb()

    await call.message.edit_text(text=text, reply_markup=markup)
