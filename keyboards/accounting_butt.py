from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from data.class_ import Accounting
from data import state


async def account_menu(index_=0, len_=int):

    kb = InlineKeyboardBuilder()
    item_id = state.db_count_dict[index_]["id"]

    if len_ == 0:

        kb.add(InlineKeyboardButton(text="Додати",
               callback_data="create_account"))

        kb.add(InlineKeyboardButton(text="Назад",
               callback_data="pass"))

        return kb.adjust(2).as_markup()
    else:
        kb3 = {
            "Видалити🗑": "delet",
            "Додати➕": "create_account",
            "Змінити✏": "chen",
            "Z-звіт": "report",
            "🔎": "serch",
            "◀Назад": "back",
            "🔄": "update",
            "⬆": "up",
            "⬇": "down",
        }

        for text, menu_name in kb3.items():

            if menu_name == 'up':
                if index_ == 0:
                    kb.add(InlineKeyboardButton(text=text, callback_data=Accounting(
                        index=len_-1).pack()))
                else:
                    kb.add(InlineKeyboardButton(text=text, callback_data=Accounting(
                        index=index_-1).pack()))

            elif menu_name == 'down':
                if index_ == len_-1:
                    kb.add(InlineKeyboardButton(text=text, callback_data=Accounting(
                        index=0).pack()))
                else:
                    kb.add(InlineKeyboardButton(text=text, callback_data=Accounting(
                        index=index_+1).pack()))

            elif menu_name == 'serch':
                kb.add(InlineKeyboardButton(text=text, callback_data="serch"))
            elif menu_name == 'report':
                kb.add(InlineKeyboardButton(text=text, callback_data="report"))

            elif menu_name == 'delet':
                kb.add(InlineKeyboardButton(
                    text=text, callback_data=f"dlt_element_{item_id}"))

            elif menu_name == 'chen':
                kb.add(InlineKeyboardButton(
                    text=text, callback_data=f"chen_elem_{item_id}"))

            elif menu_name == 'create_account':
                kb.add(InlineKeyboardButton(
                    text=text, callback_data="create_elem"))

            elif menu_name == 'back':
                kb.add(InlineKeyboardButton(
                    text=text, callback_data="back_to_main"))

            elif menu_name == 'update':
                kb.add(InlineKeyboardButton(text=text, callback_data="update"))

        return kb.adjust(3, 2, 4).as_markup()
