from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton

from loader import dp, bot


@dp.inline_handler(state="*")
async def invite(query: InlineQuery):
    bot_username = (await bot.me).username

    await query.answer(
        results=[
            InlineQueryResultArticle(
                id=str(query.from_user.id),
                title='📢 Пригласить друга!',
                input_message_content=InputTextMessageContent(
                    message_text="🎯 Биржа Wildberries  - продвижение, заработок.\n\n"
                                 "🔥Выкуп\n"
                                 "❤️Добавить в избранное\n"
                                 "💬Выкуп с отзывом и добавлением в избранное\n\n"
                                 "Партнерская программа:\n"
                                 "- привлекайте друзей и получайте по текучей ставке 20.00%"
                                 " на баланс от пополнения по вашей реферальной ссылке.\n"
                                 "- твоему другу +10.00% к балансу при первом пополнении.\n\n"
                                 "💰 Получай товары за задания!\n\n"
                                 "⚡️ У нас ты можешь привязать неограниченное кол-во аккаунтов"
                ),
                description="Нажмите, чтобы пригласить друга",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton("Запустить бота",
                                                 url=f"https://t.me/{bot_username}?start={query.from_user.id}")
                        ]
                    ]
                )
            )]
    )
