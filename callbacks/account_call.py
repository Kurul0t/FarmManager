from aiogram import Router, Bot, types
from aiogram.types import CallbackQuery, FSInputFile


from data.class_ import Accounting
from data import state
# from data.state import db_count_dict
from keyboards import accounting_butt
from keyboards import inline_butt
from handlers import processor


router = Router()


@router.callback_query(Accounting.filter())
async def handle_menu_callback(callback: CallbackQuery, callback_data: Accounting):

    await callback.answer()
    user_id =callback.from_user.id
    # state.must_del[user_id].clear()

    # print(state.db_count_dict)
    # -------------------
    len_ = len(state.db_count_dict)

    text = await processor.text_(callback_data.index)

    rm = await accounting_butt.account_menu(callback_data.index, len_)

    msg = await callback.message.edit_text(text, reply_markup=rm)
    await callback.answer()

    if msg.message_id not in state.must_del[user_id]:
        state.must_del[user_id].append(msg.message_id)


@router.callback_query(lambda c: c.data in ["serch", "back_to_main", "dlt_element", "stop_dlt", "update", "not_remind", "not_chen", "create_elem", "not_edd", "report"])
async def process_button(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    if callback.data == "serch":

        state.note_stat[user_id] = 5
        msg = await bot.send_message(user_id, "Введіть код продукту або його повну назву")
        state.must_del[user_id].append(msg.message_id)

    elif callback.data == "back_to_main":
        menu = inline_butt.farm_menu
        if user_id in state.users.values():
            await callback.message.edit_text("Головне меню\n\nЩо би ви хотіли зробити?", reply_markup=menu)

    elif callback.data == "stop_dlt":
        await callback.message.answer("Все окей, інкубація продовжується")
        state.note_stat[user_id] = 0

    elif callback.data == "update":
        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        await processor.update_dcd()

        len_ = len(state.db_count_dict)

        text = await processor.text_(0)
        rm = await accounting_butt.account_menu(0, len_)
        m = await bot.send_message(user_id, "Таблицю оновлено✅")
        msg = await bot.send_message(user_id, text, reply_markup=rm)
        state.must_del[user_id].append(msg.message_id)
        state.must_del[user_id].append(m.message_id)
        await callback.answer()
    elif callback.data == "not_remind":
        state.no_remind_dict.extend(state.dict_remind)
        state.dict_remind.clear()
        await callback.message.answer("Нагадування вимкнено")
        print(state.dict_remind)
        print(state.no_remind_dict)
    elif callback.data == "not_chen":

        state.note_stat[user_id] = 0
        len_ = len(state.db_count_dict)

        text = await processor.text_(0)
        rm = await accounting_butt.account_menu(0, len_)

        await callback.message.edit_text(text, reply_markup=rm)

        await callback.answer()
    elif callback.data == "create_elem":

        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        state.note_stat[user_id] = 8

        rm = inline_butt.stop_add_elem

        msg = await callback.message.answer("Введіть назву нового продукту", reply_markup=rm)

        state.must_del[user_id].append(msg.message_id)

    elif callback.data == "not_edd":
        state.note_stat[user_id] = 0

        if user_id in state.create_new_elem:
            del state.create_new_elem[user_id]

        await callback.answer('Скасовано')
        len_ = len(state.db_count_dict)

        text = await processor.text_(0)
        rm = await accounting_butt.account_menu(0, len_)
        await callback.message.edit_text(text, reply_markup=rm)
        state.note_stat[user_id] = 0
    elif callback.data == "report":
        file_path, current_time = await processor.report_()
        await callback.message.answer_document(
            document=FSInputFile(file_path),
            caption=f"📊 Таблиця інвентаризації у Excel\nСтаном на {current_time}"
        )


@router.callback_query(lambda callback_query: callback_query.data.startswith("dlt_element_") or callback_query.data.startswith("chen_elem_"))
async def handle_menu_callback(callback: CallbackQuery, bot: Bot):

    user_id = callback.from_user.id

    if callback.data.startswith("dlt_element_"):
        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        item_id = int(callback.data.split("_")[2])
        print(item_id)

        response = state.supabase.table("accounting").select(
            "name").eq("id", item_id).execute()

        name = response.data[0]["name"]

        rm = inline_butt.stop_dlt
        msg = await bot.send_message(user_id, f"Ви впевнені, що хочете видалити елемент {name} з бази?\nДля підтвердження введіть 'так'", reply_markup=rm)

        state.must_del[user_id].append(msg.message_id)

        state.item_id_to_del[user_id] = item_id
        state.note_stat[user_id] = 6

    elif callback.data.startswith("chen_elem_"):

        for i in state.must_del[user_id]:
            await bot.delete_message(chat_id=user_id, message_id=i)
        state.must_del[user_id].clear()

        item_id = int(callback.data.split("_")[2])
        print(item_id)

        response = state.supabase.table("accounting").select(
            "name").eq("id", item_id).execute()

        name = response.data[0]["name"]

        rm = inline_butt.stop_chen_elem
        msg = await bot.send_message(user_id, f"{name}\n❗Увага❗ \nВи можете змінити лише кількість продукту\n\n(Ви можете ввести +число, -число або оновлене число)", reply_markup=rm)
        state.must_del[user_id].append(msg.message_id)
        state.item_id_to_chen[user_id] = item_id
        state.note_stat[user_id] = 7
