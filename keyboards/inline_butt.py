from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.class_ import Accounting


fitback_meneger = InlineKeyboardMarkup(
    inline_keyboard=[
        [

            InlineKeyboardButton(
                text="Зв'язатися з оператором📞", url=f"tg://user?id=6473993763")

        ]
    ]
)


farm_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Запуск інкубатора",
                              callback_data="add_date")],
        [InlineKeyboardButton(text="Відстеження прогресу",
                              callback_data="check_date")],
        [InlineKeyboardButton(text="Інструкція інкубації",
                              callback_data="tabl_incub")],

    ]
)

"""        [InlineKeyboardButton(text="Птахи",
                              callback_data="quail_dict")]"""

brk = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Перервати інкубацію",
                              callback_data="brk")],
        [InlineKeyboardButton(text="Назад",
                              callback_data="back_to_main")]
    ]
)

zapusck = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Запуск інкубатора",
                              callback_data="add_date")],
        [InlineKeyboardButton(text="Назад",
                              callback_data="back_to_main")]
    ])


stop_brk = InlineKeyboardMarkup(
    inline_keyboard=[
                    [InlineKeyboardButton(text="Скасувати переривання",
                                          callback_data="stop_brk")]
    ]
)


cans = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вимкнути оновлення",
                              callback_data="cans_qwiz")]
    ])


stop_dlt = InlineKeyboardMarkup(
    inline_keyboard=[
                    [InlineKeyboardButton(text="Скасувати видалення",
                                          callback_data="stop_dlt")]
    ]
)

not_remind = InlineKeyboardMarkup(
    inline_keyboard=[
                    [InlineKeyboardButton(text="❌Не нагадувати❌",
                                          callback_data="not_remind")]
    ]
)

stop_chen_elem = InlineKeyboardMarkup(
    inline_keyboard=[
                    [InlineKeyboardButton(text="Скасувати",
                                          callback_data="not_chen")]
    ]
)

stop_add_elem = InlineKeyboardMarkup(
    inline_keyboard=[
                    [InlineKeyboardButton(text="Скасувати",
                                          callback_data="not_edd")]
    ]
)
