from aiogram import Bot
import pytz
from datetime import datetime, timedelta
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

# num_formula: 1- к-ть днів корму при оновлені к-ті корму
#              2- к-ть корму, оновлення вночі


async def formulаs(num_formula: int, count_feed, count_quail, avrg_con):
    if num_formula == 1:
        formul = count_feed/(count_quail*avrg_con)
    elif num_formula == 2:
        formul = count_feed-(count_quail*avrg_con)
    return formul


async def und_over():
    response = state.supabase.table(
        "quails").select("adge, count").execute()
    rows = response.data
    over_30 = sum(row["count"] for row in rows if row["adge"] > 30)
    under_30 = sum(row["count"] for row in rows if row["adge"] <= 30)
    return over_30, under_30


async def report_():
    # 1. Створюємо новий Excel-файл
    wb = Workbook()
    ws = wb.active
    ws.title = "Звіт"

    # 2. Записуємо заголовки
    ws.append(["Назва", "Код", "Кількість"])

    # 3. Дані беремо зі state.db_count_dict
    for row in state.db_count_dict:
        count = f"{row['count']}{row['mesur']}"
        ws.append([row['name'], row['code'], count])

    # Автоматичне визначення ширини стовпця "Назва" (A)
    max_length = 0
    for cell in ws['A']:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))

    ws.column_dimensions['A'].width = max_length + 2
    # 4. Зберігаємо файл
    now = datetime.now(UA_TZ)
    today_str = now.strftime("%d_%m_%Y")
    current_time = now.strftime("%d_%m_%Y (%H:%M)")
    file_path = f"report_{today_str}.xlsx"
    wb.save(file_path)
    return file_path, current_time


async def text_(index):
    text = "ТАБЛИЦЯ ОБЛІКУ\n"

    over_30, under_30 = await und_over()

    for i, value in enumerate(state.db_count_dict):
        if i == index:
            if value['code'].startswith("К-5"):
                if value['code'].startswith("К-51"):
                    d = await formulаs(1, value['count'], under_30, 0.012)

                elif value['code'].startswith("К-52"):
                    d = await formulаs(1, value['count'], over_30, 0.043)
                days = f" -> {int(d)}дн."
            else:
                days = ""
            text += f"->  {value['name']}\n--------\ncount: {value['count']}{value['mesur']}{days}\n--------\n"
        else:
            text += f"      {value['name']}\n"
    return text


async def update_dcd():
    response = state.supabase.table(
        "accounting").select("*").execute()

    state.db_count_dict = [{
        "id": row["id"],
        "name": row["name"],
        "count": row["count"],
        "mesur": row["mesur"],
        "code": row["code"]
    }
        for i, row in enumerate(response.data)]
    # print(state.db_count_dict)


async def create_remind_text(day, what_):

    text = f"СЬогодні {day}-й день, {what_}"

    return text


async def check_periodically(bot: Bot):
    # users = os.environ.get("USERS_ID")
    # user_id = 1030040998
    while True:
        now = datetime.now(UA_TZ)
        saved_date = datetime.strptime(
            data_of_start_incub["date"], "%d.%m.%Y")

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
            over_30, under_30 = await und_over()
            text = ""
            for i, value in enumerate(state.db_count_dict):
                if value['code'].startswith("К-5"):
                    if value['code'].startswith("К-51"):
                        d = await formulаs(1, value['count'], under_30, 0.012)

                    elif value['code'].startswith("К-52"):
                        d = await formulаs(1, value['count'], over_30, 0.043)
                    d = int(d)

                    if d <= 7:
                        if value["name"] not in state.no_remind_dict and value["name"] not in state.dict_remind:
                            state.dict_remind.append(value["name"])
                            text += f"{value['name']}: {value['count']}кг -> {d}дн.\n"

                        elif value["name"] not in state.no_remind_dict and value["name"] in state.dict_remind:
                            text += f"{value['name']}: {value['count']}кг -> {d}дн.\n"

            if text != "":
                """for user_id in state.users.values():
                    if state.must_del[user_id]:
                        for i in state.must_del[user_id]:
                            await bot.delete_message(chat_id=user_id, message_id=i)
                        state.must_del[user_id].clear()"""

                te = "УВАГА!\nЗакінчуються запаси корму:\n"
                te += text
                rm = inline_butt.not_remind

                for CHAT_ID in state.users.values():

                    msg = await bot.send_message(CHAT_ID, te, reply_markup=rm)

                    state.must_del[CHAT_ID].append(msg.message_id)

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

        elif now.hour == 00 and now.minute == 00:  # 00:00
            # має бути опівночі

            # state.supabase.rpc("increment_all_adge").execute()
            rows = state.worksheet_1.get_all_values()

            for row in rows[1:]:
                col = row[10]
                if col.isdigit():
                    count = int(col)
                    if count > 0:
                        print(row[4], row[8], row[10])
                        date = row[4].strip()
                        adge = int(row[8])
                        date_iso = datetime.strptime(
                            date, "%d.%m.%Y").date().isoformat()
                        result = state.supabase.table("quails").select(
                            "*").eq("were_born", date_iso).execute()
                        if len(result.data) == 0:
                            state.supabase.table("quails").insert({
                                "were_born": date_iso,
                                "count": count,
                                "adge": adge  # якщо earnings = age, дивись що потрібно
                            }).execute()
                            print(f"[ADD] {date_iso} — count: {count}")
                        else:
                            existing = result.data[0]["count"]
                            if existing != count:
                                state.supabase.table("quails").update(
                                    {"count": count}).eq("date", date).execute()
                                print(
                                    f"Оновлено count для {date}: {existing} -> {count}")
                            else:
                                print(f"Без змін: {date}")

            for user_id in state.users.values():

                if state.must_del[user_id]:
                    for i in state.must_del[user_id]:
                        await bot.delete_message(chat_id=user_id, message_id=i)
                    state.must_del[user_id].clear()

                menu = inline_butt.farm_menu

                msg = await bot.send_message(user_id, "Головне меню\n\nЩо би ви хотіли зробити?", reply_markup=menu)
                # state.must_del = msg.message_id
                state.must_del[user_id].append(msg.message_id)

            over_30, under_30 = await und_over()

            for i, value in enumerate(state.db_count_dict):
                if value['code'].startswith("К-5"):
                    if value['code'].startswith("К-51"):
                        d = await formulаs(2, value['count'], under_30, 0.012)

                    elif value['code'].startswith("К-52"):
                        d = await formulаs(2, value['count'], over_30, 0.043)

                    state.supabase.table("accounting") \
                        .update({"count": d}) \
                        .eq("id", value["id"]) \
                        .execute()

            await update_dcd()

        if cur_text != "":

            """for user_id in state.users.values():
                if state.must_del[user_id]:
                    for i in state.must_del[user_id]:
                        await bot.delete_message(chat_id=user_id, message_id=i)
                    state.must_del[user_id].clear()"""

            for CHAT_ID in state.users.values():

                msg = await bot.send_message(CHAT_ID, cur_text)

                state.must_del[CHAT_ID].append(msg.message_id)

        await asyncio.sleep(60)
