
import asyncio
import logging
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.bot import DefaultBotProperties
# from dotenv import load_dotenv

from keyboards import inline_butt
from data import state
from handlers import command, in_the_start, processor
from callbacks import incub_call, account_call

# load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


"""creds_path = os.environ.get("CREDS_PATH", "credentials.json")

if not os.path.exists(creds_path):
        raise ValueError(f"Файл credentials.json не знайдено")

try:
        with open(creds_path, "r") as f:
            creds_dict = json.load(f)
        logger.info("Файл credentials.json успішно зчитано")

        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict, state.SCOPE)
        logger.info("Облікові дані успішно створено")
except Exception as e:
        logger.error(
            "Помилка при обробці credentials.json або створенні облікових даних: %s", e)
        raise

client = gspread.authorize(creds)

    # Відкриття Google таблиціDA
KEY_1 = os.environ.get("KEY_1")
KEY_2 = os.environ.get("KEY_2")

sheet_1 = client.open_by_key(KEY_1)
sheet_2 = client.open_by_key(KEY_2)

worksheet_1 = sheet_2.get_worksheet(1)
worksheet_2 = sheet_2.get_worksheet(0)"""

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

            m = await bot.send_message(CHAT_ID, "Роботу бота відновлено")
            state.must_del[CHAT_ID].append(m.message_id)

        await dp.start_polling(bot)
    finally:

        logging.info("Бот зупинено.")

        rm = inline_butt.fitback_meneger

        for user_id, num in state.user_phon_number.items():
            await bot.send_message(user_id, "Повідомляємо Вас, що бот тимчасово не працюватиме через оновлення системи.\n\nДля замовлення нашої продукції, ви можете зв'язатися з нашим оператором↘", reply_markup=rm)

        for CHAT_ID in state.users.values():

            for i in state.must_del[CHAT_ID]:
                await bot.delete_message(chat_id=CHAT_ID, message_id=i)

            await bot.send_message(CHAT_ID, "Бот тимчасово не працює\n\nПісля відновлення роботи, видаліть дане повідомлення самостійно")

        # state.conn.close()


if __name__ == "__main__":
    asyncio.run(main())
