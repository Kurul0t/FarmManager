
from aiogram import Router, Bot, types

from data import state

from handlers.incubation import add_date, days_until_date
from keyboards import inline_butt
from data.state import worksheet_1,worksheet_2

router = Router()


@router.callback_query(lambda c: c.data in ["pass"])
async def process_button(callback: types.CallbackQuery, bot: Bot):
	if callback.data == "add_date":
		pass