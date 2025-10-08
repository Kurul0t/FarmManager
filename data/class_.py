from aiogram.filters.callback_data import CallbackData


# ----------------

class Menu_callback(CallbackData, prefix="menu"):
    level: int
    menu_name: str
    # description: str


class Pagination(CallbackData, prefix="pag"):
    page: int
    select: int = 0
    st: int = 0


class Cart_call(CallbackData, prefix="cart"):
    page: int
    menu_name: str


class Pre_pag(CallbackData, prefix="pre_pag"):
    page: int


class List_ord(CallbackData, prefix="ord"):
    page: int


class Activ(CallbackData, prefix="act"):
    page: int


class Hist(CallbackData, prefix="hist"):
    page: int


# ----------------------

class Accounting(CallbackData, prefix="Account"):
    index: int
