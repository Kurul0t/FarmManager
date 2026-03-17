
import asyncio
import logging
import os
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.bot import DefaultBotProperties


from keyboards import inline_butt
from data import state
from handlers import command, in_the_start, processor
from callbacks import incub_call, account_call

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено")

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()


async def main() -> None:

    dp.include_routers(command.router, incub_call.router, account_call.router)

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("запуск перевірки")


    # asyncio.create_task(start_task())
    asyncio.create_task(processor.check_periodically(bot))

    try:
        await in_the_start.on_startup()

        for CHAT_ID in state.users.values():

            await bot.send_message(CHAT_ID, "Роботу бота відновлено")


        await dp.start_polling(bot)
    finally:

        logging.info("Бот зупинено.")

        rm = inline_butt.fitback_meneger

        for user_id, num in state.user_phon_number.items():
            await bot.send_message(user_id, "Повідомляємо Вас, що бот тимчасово не працюватиме через оновлення системи.\n\nДля замовлення нашої продукції, ви можете зв'язатися з нашим оператором↘", reply_markup=rm)

        for CHAT_ID in state.users.values():



            await bot.send_message(CHAT_ID, "Бот тимчасово не працює\n\nПісля відновлення роботи, видаліть дане повідомлення самостійно")

        # state.conn.close()


if __name__ == "__main__":
    asyncio.run(main())
