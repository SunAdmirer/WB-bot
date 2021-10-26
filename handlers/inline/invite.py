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
                    message_text="Текст"
                ),
                description="Нажмите, что бы пригласить друга",
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
