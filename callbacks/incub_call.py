
from aiogram import Router, Bot, types

from data import state

from handlers.incubation import add_date, days_until_date
from keyboards import inline_butt
from data.state import worksheet_1, worksheet_2

router = Router()


@router.callback_query(lambda c: c.data in ["add_date", "Arrngmnt", "check_date", "brk", "stop_brk", "tabl_incub", "cans_qwiz"])
async def process_button(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if callback.data == "add_date":
        await add_date(callback, bot)
    elif callback.data == "check_date":
        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        rows = worksheet_1.get_all_values()

        last_row = rows[-1]

        delta_day_1, delta_day_2 = await days_until_date(last_row[2], last_row[4])
        if isinstance(delta_day_2, str):
            await callback.message.answer(delta_day_2)
            return
        line_1 = "-" * delta_day_1 if delta_day_1 >= 0 else ""
        line_2 = "-" * delta_day_2 if delta_day_2 >= 0 else ""
        # message = f"Вилуп впродож сьогоднішнього дня!" if delta_day_2 < 0 else f"📍{line_1}🥚{line_2}🐣\nДнів до вилупу: {delta_day_2}"
        brk = inline_butt.brk
        zapusck = inline_butt.zapusck

        state.must_del[user_id].clear()

        if last_row[0] == "*":
            message = "Активної інкубації не виявлено"
            ms = await bot.send_message(user_id, message, reply_markup=zapusck)
            state.must_del[user_id].append(ms.message_id)
        elif delta_day_2 == 0:
            msg = "Вилуп впродож сьогоднішнього дня!"

            m = await bot.send_message(user_id,
                                       f"Дата закладання: {last_row[2]}\n"
                                       f"Дата вилупу: {last_row[4]}\n"
                                       f"Закладено, шт: {last_row[5] or 'не вказано'}\n\n"
                                       f"{message}", reply_markup=brk)
            state.must_del[user_id].append(m.message_id)
        else:
            msg = f"📍{line_1}🥚{line_2}🐣\nДнів до вилупу: {delta_day_2}"
            m = await bot.send_message(user_id,
                                       f"Сьогодні {delta_day_1}-й день\n"
                                       f"Дата закладання: {last_row[2]}\n"
                                       f"Дата вилупу: {last_row[4]}\n"
                                       f"Закладено, шт: {last_row[5] or 'не вказано'}\n\n"
                                       f"{msg}", reply_markup=brk)
            state.must_del[user_id].append(m.message_id)

    elif callback.data == "brk":

        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        rows = state.worksheet_1.get_all_values()
        last_row = rows[-1]
        if last_row[0] != "*":

            state.note_stat[user_id] = 2

            stop_brk = inline_butt.stop_brk

            ms = await callback.message.answer("Ви впевнені, що хочете перевати інкубацію?\n(Для підтвердження напишіть 'так')", reply_markup=stop_brk)
            state.must_del[user_id].append(ms.message_id)

    elif callback.data == "stop_brk":

        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        msg = await callback.message.answer("Все окей, інкубація продовжується")
        state.must_del[user_id].append(msg.message_id)
        state.note_stat[user_id] == 0

    elif callback.data == "tabl_incub":

        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()
        photo_inc = state.photo_incubation
        msg = await callback.message.answer_photo(photo_inc)
        state.must_del[user_id].append(msg.message_id)

    elif callback.data == "cans_qwiz":
        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        state.note_stat[user_id] = 4
        msg = await callback.message.answer("Чи усіх циплаків було пораховано?\n(Для підтвердження/спростування напиши так/ні)")

        state.must_del[user_id].append(msg.message_id)

    """elif callback.data == "Arrngmnt":
        t = await Arrangement()
        await bot.send_message(user_id, f"Розміщення перепелів", reply_markup=t)"""
