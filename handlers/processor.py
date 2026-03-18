from aiogram import Bot
import pytz
from datetime import datetime, timedelta, date
import logging
import asyncio
from openpyxl import Workbook

# ------------------
# шось написав

from data.state import data_of_start_incub
from data import state
from keyboards import inline_butt
# ------------------
#
UA_TZ = pytz.timezone("Europe/Kyiv")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ddtt = date

# num_formula: 1- к-ть днів корму при оновлені к-ті корму
#              2- к-ть корму, оновлення вночі




async def create_remind_text(day, what_):

    text = f"СЬогодні {day}-й день, {what_}"

    return text


def weekday_in_days_(n=3):

    weekday_in_days = date.today().isoweekday()+3
    return weekday_in_days % 7


async def check_periodically(bot: Bot):
    # users = os.environ.get("USERS_ID")
    # user_id = 1030040998
    while True:
        now = datetime.now(UA_TZ)
        date_str = state.data_of_start_incub.get("date")

        if not date_str:
            logger.warning("No start incub date yet")
            await asyncio.sleep(60)
            continue
        
        saved_date = datetime.strptime(date_str, "%d.%m.%Y")

        print("saved_date", saved_date)
        today_str = now.strftime("%d.%m.%Y")

        date_plus_2 = (saved_date + timedelta(days=2)
                       ).strftime("%d.%m.%Y")

        date_plus_8 = (saved_date + timedelta(days=8)
                       ).strftime("%d.%m.%Y")

        date_plus_9 = (saved_date + timedelta(days=9)
                       ).strftime("%d.%m.%Y")

        date_plus_14 = (saved_date + timedelta(days=14)
                        ).strftime("%d.%m.%Y")

        date_plus_15 = (saved_date + timedelta(days=15)
                        ).strftime("%d.%m.%Y")

        date_plus_16 = (saved_date + timedelta(days=16)
                        ).strftime("%d.%m.%Y")

        date_plus_17 = (saved_date + timedelta(days=17)
                        ).strftime("%d.%m.%Y")

        cur_text = ""

  

        if (now.hour == 12 and now.minute == 00):  # 12:00


            # ---------------------------------

            if "date" in data_of_start_incub:

                if date_plus_8 == today_str:

                    cur_text = await create_remind_text(8, "завтра потрібно зменшити вологу до 40% та почати провітрювати інкубатор")

                elif date_plus_14 == today_str:

                    cur_text = await create_remind_text(14, "завтра потрібно зменшити температуру до 37.4, збільшити вологу до 75-80% та викласти яйця на дно інкубатора")

                elif date_plus_16 == today_str:

                    cur_text = "Сьогодні 16-й день інкубації, скоро почнеться вилуп🥳"

                else:
                    print("❌ Дата не збігається.")

            else:
                print("Час перевірки! Але дати немає.")

        # відправка повідомлення в той день зранку і ввечері

        elif (now.hour == 6 and now.minute == 00) or (now.hour == 20 and now.minute == 00):  # 6:00 20:00

            if "date" in data_of_start_incub:

                if date_plus_2 == today_str and (now.hour == 6 and now.minute == 00):

                    cur_text = await create_remind_text(2, "потрібно увімкнути перевертання")

                elif date_plus_9 == today_str:

                    cur_text = await create_remind_text(9, "потрібно зменшити вологу до 40% та почати провітрювати інкубатор")

                elif date_plus_15 == today_str:

                    cur_text = await create_remind_text(15, "потрібно зменшити температуру до 37.4, збільшити вологу до 75-80% та викласти яйця на дно інкубатора")

                else:
                    print("❌ Дата не збігається.")

            else:
                print("Час перевірки! Але дати немає.")

        elif now.hour == 10 and now.minute == 00:  # 10:00

            if "date" in data_of_start_incub:

                if date_plus_17 == today_str:

                    cur_text = "Сьогодні 17-й день інкубації, день вилупу🥳"

                    rows = state.worksheet_1.get_all_values()
                    last_row_index = len(rows)

                    state.chus_quail[1] = last_row_index
                    state.worksheet_1.update_cell(last_row_index, 1, "*")
                    state.st[1] = 0
                    # await cycl()

                else:
                    print("❌ Дата не збігається.")
            else:
                print("Час перевірки! Але дати немає.")



        if cur_text != "":



            for CHAT_ID in state.users.values():

                await bot.send_message(CHAT_ID, cur_text)


        await asyncio.sleep(60)
