from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.class_ import Menu_callback, Cart_call
from data import state


async def main_menu(user_id=None):
    kb = InlineKeyboardBuilder()
    buttons = {
        "Товари": "catalog",
        "Кошик": "cart",
        "Про нас": "about",
        "Профіль": "cabinet"
    }

    for text, menu_name in buttons.items():
        if menu_name == 'catalog':
            kb.add(InlineKeyboardButton(text=text, callback_data=Menu_callback(
                level=1, menu_name=menu_name).pack()))
        elif menu_name == 'cart':

            if user_id in state.cart_receipt and state.cart_receipt[user_id]:
                kb.add(InlineKeyboardButton(text=text, callback_data=Cart_call(
                    page=0, menu_name=menu_name).pack()))
            else:
                kb.add(InlineKeyboardButton(text=text, callback_data=Menu_callback(
                    level=3, menu_name=menu_name).pack()))
        elif menu_name == 'about':
            kb.add(InlineKeyboardButton(text=text, callback_data=Menu_callback(
                level=4, menu_name=menu_name).pack()))
        elif menu_name == 'cabinet':
            kb.add(InlineKeyboardButton(text=text, callback_data="cabinet"))
    return kb.adjust(2, 1, 1).as_markup()


async def about():

    kb = InlineKeyboardBuilder()

    buttons = {

        "Зв'язатися з нами📞": "contact",
        "Назад": "back"
    }

    '''"Досягнення🏆": "achiv",'''

    for text, menu_name in buttons.items():
        if menu_name == 'back':
            kb.add(InlineKeyboardButton(text=text, callback_data=Menu_callback(
                level=0, menu_name=menu_name).pack()))
        elif menu_name == 'contact':
            kb.add(InlineKeyboardButton(
                text=text, url=f"tg://user?id=6473993763"))
        elif menu_name == 'achiv':
            kb.add(InlineKeyboardButton(text=text, callback_data=Menu_callback(
                level=5, menu_name=menu_name).pack()))
    return kb.adjust(1).as_markup()
