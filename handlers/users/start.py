from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loguru import logger

from filters import NotBanned
from handlers.users.main_menu import main_menu
from loader import dp, bot
from utils.db_api.commands.referrals_cmds import add_recruiter_and_recruit
from utils.db_api.commands.users_cmds import add_user, get_user_by_telegram_id

from utils.db_api.models import Users
from re import compile


# Start with deep_link
@dp.message_handler(NotBanned(), CommandStart(deep_link=compile(r"\d+")), state="*")
async def bot_start_with_deep_link(message: types.Message, user: Users, state: FSMContext, **kwargs):
    # Регистрация пользователя
    if user is None:
        # Добавление пользователя
        recruit: Users = await add_user(telegram_id=message.chat.id, username=message.from_user.username)

        # Telegram id рекрутера
        deep_link = int(message.get_args())

        # Получаем рекрутера
        recruiter: Users = await get_user_by_telegram_id(telegram_id=deep_link)

        # Если deep_link был верным и указывал на сущствующего пользователя
        if recruiter:
            # Добавление рекрутера и рекрута
            await add_recruiter_and_recruit(recruiter=recruiter, recruit=recruit)

            # Бонус рекрутеру и рекруту
            # await add_bonus_ref(recruiter_id=recruiter.pk, recruit_id=recruit.pk)

            # Сообщение для рекрута
            await message.answer("Ты пришел по реферальной программе")

            # Стартовое сообщение №1
            await message.answer("Стартовое сообщение №1")

            # Стартовое сообщение №2
            await message.answer("Стартовое сообщение №2")

            # Сообщение для рекрутера
            try:
                markup = ''
                await bot.send_message(chat_id=recruiter.telegram_id,
                                       text="У вас новый рекрут",
                                       reply_markup=markup)
            except Exception as ex:
                logger.warning(ex)

    # Переход в главное меню (выбор предмета)
    await main_menu(message=message, user=user, state=state)


# Обычный start
@dp.message_handler(NotBanned(), CommandStart(), state="*")
async def bot_start(message: types.Message, user: Users, state: FSMContext, **kwargs):
    # Регистрация пользователя
    if user is None:
        # Добавление пользователя
        user = await add_user(telegram_id=message.chat.id, username=message.from_user.username)

        # Стартовое сообщение №1
        await message.answer("Стартовое сообщение №1")

        # Стартовое сообщение №2
        await message.answer("Стартовое сообщение №2")

    # Переход в главное меню (выбор предмета)
    await main_menu(message=message, user=user, state=state)
