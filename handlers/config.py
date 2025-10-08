import logging
import os
import json
import gspread
from dotenv import load_dotenv


from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.bot import DefaultBotProperties


import data.state as state

load_dotenv()
logger = logging.getLogger(__name__)



