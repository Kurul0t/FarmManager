
from aiogram import Router, Bot, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ContentType
import os
from urllib.parse import quote


from keyboards import reply_butt, main_menu_about, inline_butt, accounting_butt
from data import state
from handlers import processor
from handlers.incubation import send_note, cycl
from data.state import st, note_stat, worksheet_1, worksheet_2


secret_command = os.environ.get("SECRET_COMMAND")


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, bot: Bot) -> None:

    # Надсилаємо фото через answer_photo
    # await message.answer_photo(photo=photo,reply_markup=butt)
    user_id = message.from_user.id
    print(user_id)

    markup = reply_butt.send_number_start
    keyboard = reply_butt.start

    if user_id in state.users.values():
        await message.answer('Привіт, це бот мініферми "Степова перепілка"', reply_markup=keyboard)
    else:
        """username = "kurulot"  # тут юзернейм того, кому треба написати
        text = "Йдем в кіно)"
        # формуємо лінк
        link = f"https://t.me/{username}?text={quote(text)}"

        await bot.send_message(
            chat_id=user_id,
            text=(
                "Супер! Сподіваюсь, гарно проведете час 🙌\n\n"
                f'Починай спілкуватися 👉 <a href="{link}">Тицни</a>'
            ),
            parse_mode="HTML",
            disable_web_page_preview=True
        )"""
        await bot.send_message(user_id, text='Вас вітає міні-ферма "Степова перепілка"\nЩоб почати користувася ботом, зареєструйтесь, будь ласка↘', reply_markup=markup)


@router.message(Command(secret_command))
async def hidden_command(message: Message):
    user_id = message.from_user.id
    if user_id in state.users.values():
        await message.answer("Це прихована команда. Лише для обраних 😉")


@router.message(F.contact)
async def contact_handler(message: Message, bot: Bot):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    name = message.from_user.full_name
    state.user_phon_number[user_id] = {}
    state.user_phon_number[user_id] = phone

    with state.conn.cursor() as cur:

        cur.execute("""
                INSERT INTO users (name, user_id,phone)
                VALUES (%s,%s, %s)
                ON CONFLICT (user_id) DO NOTHING;
            """, (name, user_id, phone))
        state.conn.commit()

    rm = await main_menu_about.main_menu(user_id)
    # Надсилаємо фото через send_photo
    # await bot.send_photo(chat_id=user_id, photo=photo)
    markup = reply_butt.main_menu

    await bot.send_message(user_id, text='Дякую, тепер можете користуватися ботом', reply_markup=markup)

    await bot.send_photo(user_id, photo=state.photo[0], caption=state.main_description[0], reply_markup=rm)


@router.message(F.text.lower() == "меню")
async def reply_action(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    # user_id == 1030040998 or
    # if user_id == 1995558338:
    if user_id not in note_stat:
        note_stat[user_id] = 0

    menu = inline_butt.farm_menu
    if user_id in state.users.values():
        await message.delete()
        if state.must_del[user_id]:
            for i in state.must_del[user_id]:
                await bot.delete_message(chat_id=user_id, message_id=i)
            state.must_del[user_id].clear()
        msg = await bot.send_message(user_id, "Головне меню\n\nЩо би ви хотіли зробити?", reply_markup=menu)
        # state.must_del = msg.message_id
        state.must_del[user_id].append(msg.message_id)


@router.message(lambda message: message.content_type == ContentType.TEXT)
async def handle_text(message: Message, bot: Bot):
    user_id = message.from_user.id
    if 1111 not in note_stat:
        note_stat[1111] = 0

    if user_id not in note_stat:
        note_stat[user_id] = 0

    if note_stat[user_id] == 1:
        await send_note(user_id, message, bot)
        note_stat[user_id] = 0
    elif note_stat[user_id] == 2:
        state.must_del[user_id].append(message.message_id)
        if message.text.lower() == "так":
            note_stat[user_id] = 3

            for i in state.must_del[user_id]:
                await bot.delete_message(chat_id=user_id, message_id=i)
            state.must_del[user_id].clear()
            rm = inline_butt.stop_brk
            msg = await bot.send_message(user_id, "Додай коментар, аби інші також знали причину, або введи символ ' - '", reply_markup=rm)
            state.must_del[user_id].append(msg.message_id)
        else:

            for i in state.must_del[user_id]:
                await bot.delete_message(chat_id=user_id, message_id=i)
            state.must_del[user_id].clear()
            rm = inline_butt.stop_brk
            msg = await bot.send_message(user_id, "Некоректна відповідіть\n\nВведіть 'так' для підтвердження або скасуйте", reply_markup=rm)
            state.must_del[user_id].append(msg.message_id)
            state.note_stat[user_id] = 2

    elif note_stat[user_id] == 3:

        state.must_del[user_id].append(message.message_id)

        rows = worksheet_1.get_all_values()
        last_row_index = len(rows)

        worksheet_1.update_cell(last_row_index, 1, "*")
        worksheet_1.update_cell(last_row_index, 2, "Перервано")

        comment = "відсутній" if message.text == "-" else message.text

        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        for CHAT_ID in state.users.values():
            msg = await bot.send_message(CHAT_ID, f"‼Інкубацію було перервано‼\n\nКоментар: {comment}\nХто перервав: {message.from_user.first_name or ''}{message.from_user.last_name or ''}")
            state.must_del[CHAT_ID].append(msg.message_id)

        note_stat[user_id] = 0
    elif note_stat[user_id] == 4:
        if message.text.lower() == "так":
            st[1] = 1
            note_stat[1111] = 1
            await cycl()
        elif message.text.lower() == "ні":
            await bot.send_message(user_id, "Наступне оновлення через 2 години")
        note_stat[user_id] = 0

    elif note_stat[user_id] == 5:
        stat = 0
        state.must_del[user_id].append(message.message_id)
        for i in state.must_del:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()
        for i, value in enumerate(state.db_count_dict):
            # print()
            if value["name"] == message.text or value["code"] == message.text:
                stat = 1
                text = await processor.text_(i)
                len_ = len(state.db_count_dict)
                rm = await accounting_butt.account_menu(i, len_)
                m = await bot.send_message(user_id, text, reply_markup=rm)
                state.must_del[user_id].append(m.message_id)
        if stat == 0:
            text = await processor.text_(0)
            len_ = len(state.db_count_dict)
            rm = await accounting_butt.account_menu(0, len_)
            msg = await bot.send_message(user_id, f"Продукт {message.text} не було знайдено")
            ms = await bot.send_message(user_id, text, reply_markup=rm)

            state.must_del[user_id].append(msg.message_id)
            state.must_del[user_id].append(ms.message_id)

        state.note_stat[user_id] = 0
    elif note_stat[user_id] == 6:
        await message.delete()
        for i in state.must_del:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()
        if message.text.lower() == "так":
            note_stat[user_id] = 0

            state.supabase.table("accounting").delete().eq(
                "id", state.item_id_to_del[user_id]).execute()

            await processor.update_dcd()
            # ---------------
            len_ = len(state.db_count_dict)

            text = await processor.text_(0)

            rm = await accounting_butt.account_menu(0, len_)
            # ---------------
            # await bot.send_message(user_id, "Елемент було видалено")
            m = await message.answer("🗑 Елемент видалено 🗑")

            msg = await bot.send_message(user_id, text, reply_markup=rm)
            state.must_del[user_id].append(msg.message_id)
            state.must_del[user_id].append(m.message_id)
        else:
            rm = inline_butt.stop_dlt
            msg = await message.answer("Некоректне введення\n\nВведіть 'так' або скасуйте видалення", reply_markup=rm)
            state.must_del[user_id].append(msg.message_id)

            state.note_stat[user_id] = 6
    elif note_stat[user_id] == 7:
        text = message.text.strip()

        response = state.supabase.table("accounting").select(
            "count").eq("id", state.item_id_to_chen[user_id]).execute()

        curr = float(response.data[0]["count"])
        if text[0].isdigit():
            number = float(text)

        elif text.startswith("+"):
            number = curr + float(text.lstrip("+"))

            code = state.supabase.table("accounting").select("code").eq(
                "id", state.item_id_to_chen[user_id]).execute()
            print("code", code)

            code_value = code.data[0]["code"]

            print("code_value", code_value)
            if code_value.startswith("Л-"):
                cur_count = state.supabase.table("accounting").select(
                    "count").eq(
                    "code", "Ш-67").execute()
                cur_count_value = float(cur_count.data[0]["count"])

                new_count = cur_count_value-int(text.lstrip("+"))

                state.supabase.table("accounting").update(
                    {"count": new_count}).eq("code", "Ш-67").execute()

        elif text.startswith("-"):
            number = curr - float(text.lstrip("-"))

        else:
            # помилка
            number = curr

        state.supabase.table("accounting") \
            .update({"count": number}) \
            .eq("id", state.item_id_to_chen[user_id]) \
            .execute()
        await processor.update_dcd()
        # ---------------
        len_ = len(state.db_count_dict)

        text = await processor.text_(0)

        rm = await accounting_butt.account_menu(0, len_)
        # ---------------
        await message.answer("✍ К-ть змінено ✍")

        await bot.send_message(user_id, text, reply_markup=rm)
    elif note_stat[user_id] == 8:
        await message.delete()
        for i in state.must_del:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        state.create_new_elem[user_id] = {
            "name": message.text,   # перший крок
            "code": None,
            "count": None,

        }
        rm = inline_butt.stop_add_elem
        text = f"Назва: {message.text}\n\nВведіть код продукту"
        msg = await bot.send_message(user_id, text, reply_markup=rm)
        state.must_del[user_id].append(msg.message_id)
        state.note_stat[user_id] = 9

    elif note_stat[user_id] == 9:
        await message.delete()
        for i in state.must_del:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        state.create_new_elem[user_id]['code'] = message.text
        rm = inline_butt.stop_add_elem
        text = (
            f"Назва: {state.create_new_elem[user_id]['name']}\n"f"Код: {message.text}\n\nВведіть к-ть товару або 0")
        msg = await bot.send_message(user_id, text, reply_markup=rm)
        state.must_del[user_id].append(msg.message_id)
        state.note_stat[user_id] = 10

    elif note_stat[user_id] == 10:
        await message.delete()
        for i in state.must_del:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        if message.text.isdigit():
            rm = inline_butt.stop_add_elem
            state.create_new_elem[user_id]['count'] = message.text

            text = (
                f"Назва: {state.create_new_elem[user_id]['name']}\n"
                f"Код: {state.create_new_elem[user_id]['code']}\n"
                f"К-ть: {float(message.text)}\n\n"
                "Бажаєте додати? (так)"
            )
            msg = await bot.send_message(user_id, text, reply_markup=rm)
            state.must_del[user_id].append(msg.message_id)
            state.note_stat[user_id] = 11

        else:
            state.note_stat[user_id] = 10
            msg = await message.answer("Некоректне введення к-ті\n\nВведіть ЧИСЛО або 0")
            state.must_del[user_id].append(msg.message_id)
    elif note_stat[user_id] == 11:
        await message.delete()
        for i in state.must_del:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()
        if message.text.lower() == "так":
            # -----------------------
            state.supabase.table("accounting").insert({
                "name": state.create_new_elem[user_id]["name"],
                "code": state.create_new_elem[user_id]["code"],
                # краще конвертувати в число
                "count": state.create_new_elem[user_id]["count"]
            }).execute()
            # ----------------------

            state.note_stat[user_id] = 0

            await processor.update_dcd()
            # ---------------
            len_ = len(state.db_count_dict)

            text = await processor.text_(0)

            rm = await accounting_butt.account_menu(0, len_)
            # ---------------
            msg = await bot.send_message(user_id, text, reply_markup=rm)
            state.must_del[user_id].append(msg.message_id)

            state.note_stat[user_id] = 0
        else:
            rm = inline_butt.stop_add_elem
            msg = await message.answer("Некоректне введення\n\nВведіть 'так' або скасуйте додавання", reply_markup=rm)
            state.must_del[user_id].append(msg.message_id)

            state.note_stat[user_id] = 11

    if note_stat[1111] == 1:

        last_row_index = state.chus_quail[1]
        worksheet_1.update_cell(last_row_index, 7, message.text)
        cans = inline_butt.cans
        for CHAT_ID in state.users.values():
            await bot.send_message(CHAT_ID, f"Оновлення кількості вилуплених циплаків: {message.text}", reply_markup=cans)
            # await bot.send_message(CHAT_ID, "Наступне оновлення через 2 години", reply_markup=cans)

        note_stat[1111] = 0
