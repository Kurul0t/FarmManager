
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


send_number_start = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Відправити", request_contact=True)]],
    resize_keyboard=True
)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Головне меню")]],
    resize_keyboard=True
)


start = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Меню")]],
        resize_keyboard=True
    )