import pytz
from datetime import datetime, timedelta
from aiogram import types, Bot
import logging
import asyncio


from data import state
from data.state import worksheet_1, worksheet_2, st, note_stat
from keyboards import inline_butt
UA_TZ = pytz.timezone("Europe/Kyiv")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def add_date(callback: types.CallbackQuery, bot: Bot):
    rows = worksheet_1.get_all_values()
    user_id = callback.from_user.id
    if rows and rows[-1][0] == '*':
        today_str = datetime.now(UA_TZ).strftime("%d.%m.%Y")
        state.data_of_start_incub["date"] = today_str
        today = datetime.strptime(today_str, "%d.%m.%Y")
        date_p_17 = (today + timedelta(days=17)).strftime("%d.%m.%Y")
        le = len(rows)+1
        print("rows[-1]", le)



        await callback.answer("✅Активовано запуск✅")
        await callback.message.answer("⚙Процедура запуску інкубатора⚙")

        state.note_stat[user_id] = 1

        await callback.message.answer("Яку кількість яєць було закладено?\n(Напишіть лише число)")



    else:
        await callback.answer("❌Помилка❌")
        await callback.message.answer("❌На жаль, немає вільних інкубаторів!")

        menu = inline_butt.farm_menu
        if user_id in state.users.values():
            await bot.send_message(user_id, "Головне меню\n\nЩо би ви хотіли зробити?", reply_markup=menu)



async def send_note(user_id: int, message: types.Message, bot: Bot):


    rows = worksheet_1.get_all_values()



    today_str = datetime.now(UA_TZ).strftime("%d.%m.%Y")

    le = len(rows)+1
    worksheet_1.append_row([None, "Запуск", today_str, None, f'=IF(C{le}="";"";C{le}+17)'],
                           value_input_option="USER_ENTERED")

    rows = worksheet_1.get_all_values()

    if rows and rows[-1][0] == '*':
        await bot.send_message(user_id, "⚙Виникли несправності⚙\nЗверніться до адміністратора")

    else:
        czus = message.text

        last_row_index = len(rows)

        worksheet_1.update_cell(last_row_index, 6, czus)
        worksheet_1.update_cell(last_row_index, 2, "Етап 1")

        state.data_of_start_incub["date"] = today_str

        today = datetime.strptime(today_str, "%d.%m.%Y")

        date_p_17 = (today + timedelta(days=17)).strftime("%d.%m.%Y")

        for CHAT_ID in state.users.values():
            await bot.send_message(CHAT_ID, f"Відбувся запуск інкубатора\nК-ть закладених яєць: {czus}\nОрієнтовна дата вилупу: {date_p_17}")




async def days_until_date(launch_date_str, target_date_str, date_format="%d.%m.%Y"):
    today = datetime.now(UA_TZ).date()
    start_date = datetime.strptime(launch_date_str, date_format).date()
    target_date = datetime.strptime(target_date_str, date_format).date()
    delta_1 = today - start_date
    delta_2 = target_date - today
    # Не враховуємо сьогодні
    days_1 = delta_1.days  # - (1 if delta_1.days >= 0 else 0)
    # Не враховуємо сьогодні
    days_2 = delta_2.days  # - (1 if delta_2.days >= 0 else 0)
    return days_1, days_2


async def cycl(bot: Bot):
    # st=st
    while True:
        if st[1] == 1:
            rows = worksheet_1.get_all_values()
            row = rows[-1]
            # ch = row[6]*100/row[5]
            if note_stat[1111] == 1:
                for CHAT_ID in state.users.values():
                    await bot.send_message(CHAT_ID, f"Загалом вилупилося циплаків: {row[6]}\n Відсоток вилупу: {row[7]}%")
                logger.info(f"перед {st[1]}")
            note_stat[1111] = 0
            break
        else:
            """logger.info(st[1])
            note_stat[1111] = 1
            for CHAT_ID in state.users.values():
                await bot.send_message(CHAT_ID, "Скільки циплаків вилупилося на даний момент?")"""
            await asyncio.sleep(1*3600)
