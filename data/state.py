import os
import json
import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv


from supabase import create_client

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]


creds_path = os.environ.get("CREDS_PATH", "credentials.json")

if not os.path.exists(creds_path):
    raise ValueError(f"Файл credentials.json не знайдено")

try:
    with open(creds_path, "r") as f:
        creds_dict = json.load(f)
    logger.info("Файл credentials.json успішно зчитано")

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, SCOPE)
    logger.info("Облікові дані успішно створено")
except Exception as e:
    logger.error(
        "Помилка при обробці credentials.json або створенні облікових даних: %s", e)
    raise

client = gspread.authorize(creds)

# Відкриття Google таблиціDA
KEY_1 = os.environ.get("KEY_1")
KEY_2 = os.environ.get("KEY_2")

sheet_1 = client.open_by_key(KEY_1)
sheet_2 = client.open_by_key(KEY_2)

worksheet_1 = sheet_2.get_worksheet(1)
worksheet_2 = sheet_2.get_worksheet(0)


users = {1: 1030040998, 2: 1995558338}
# users = {1: 1030040998}
# users={}

weekdays_=['ПН','ВТ','СР','ЧТ','ПТ','СБ','НД']
# -----------------------------

main_description = {
    0: "Головне меню",
    1: "Категорії",
    2: "Послуги",
    3: "Кошик",
    4: "Степова перепілка - родинна \nмініферма, яка завжди радує своїх \nклієнтів лише свіжою продукцією\n\nНижче ви можете переглянути \nнаші досягнення🏆 або зв'язатися \nз нашим оператором📞"}

tovar_description = {
    0: "Мариновані Яйця",
    1: "Маринована перепілка",
    2: "Столові Яйця",
    3: "Свіже м'ясо"}

tovar_price = {
    0: 100,
    1: 360,
    2: 50,
    3: 310}

val = {
    0: "шт",
    1: "кг",
    2: "шт",
    3: "кг"
}

pre_order = {0: "Свіже м'ясо"}
pre_order_price = {0: 310}
pre_val = {0: "кг"}


tovar_description11 = " грн\nЄ в наявності"
tovar_description12 = " грн\nОбрано"
tovar_description13 = " грн\nНемає в наявності"

tovar_description2 = "                              "

# -----------------------------------


status = {
    0: "ОЧІКУЄ",
    1: "ОБРОБЛЯЄТЬСЯ",
    2: "ОФОРМЛЕНО",
    3: "ДОСТАВЛЯЄТЬСЯ"}

st_proc = 0

photo = {}
photo2 = {}
photo3 = {}
photo_incubation = {}


data_of_start_incub = {}  # запам'ятовування дати запуску інкубатора

user_phon_number = {}  # словник номерів телефонів користувачів


note_stat = {}  # статуси для прийому тексту
st = {}  # статус скасування інкубації (1 або 0)
chus_quail = {}

# ------------------------------------------------

url = "https://kadgcljpwfdrfxnadwxt.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImthZGdjbGpwd2ZkcmZ4bmFkd3h0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjUyOTQ1OSwiZXhwIjoyMDcyMTA1NDU5fQ.UzzxSR0k8_wDKktMkQ1QS2xakTa2ODLfzcug8GQ3ikI"


supabase = create_client(url, key)

db_count_dict = None  # таблиця кількості товару(облік)

item_id_to_del = {}
dict_remind = []
no_remind_dict = []
item_id_to_chen = {}
create_new_elem = {}
# ---------------------------------------------
must_del = {}
remind_mess_del = None

#---------------------
chenge_of_feed = 30
