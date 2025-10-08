import logging
from aiogram.types import BufferedInputFile
import os
from dotenv import load_dotenv

from data import state
from data.state import worksheet_1, worksheet_2
from handlers import processor


load_dotenv()

IMAGE_FOLDER = "images"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_startup():
    print("Програма запущена. Виконання ініціалізації...")

    users_str = os.getenv("AUTHORIZED_USERS")
    if users_str:
        try:
            user_id_list = [int(uid.strip()) for uid in users_str.split(',')]

            state.users = {
                index + 1: user_id
                for index, user_id in enumerate(user_id_list)
            }
            
        except ValueError:
            print(
                "Помилка: Одне або кілька значень у AUTHORIZED_USERS не є коректними числами.")

            state.users = {}
    print(state.users)

    await processor.update_dcd()

    for user_id in state.users.values():
        state.must_del[user_id] = []

    rows = worksheet_1.get_all_values()
    # user_id = callback.from_user.id
    if rows:
        last_row = rows[-1]
        state.data_of_start_incub["date"] = last_row[2]
        logger.info(f"Останній запис:{last_row[2]}")

    t2 = len(state.tovar_description)
    t3 = len(state.pre_order)

    for i in range(7):
        image_path = os.path.join(IMAGE_FOLDER, f"{i}.jpg")
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        state.photo[i] = BufferedInputFile(
            file=image_data, filename=f"{i}.jpg")

    for i in range(t2):
        image_path = os.path.join(IMAGE_FOLDER, f"{i}11.jpg")
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        state.photo2[i] = BufferedInputFile(
            file=image_data, filename=f"{i}11.jpg")

    for i in range(t3):
        image_path = os.path.join(IMAGE_FOLDER, f"{i}21.jpg")
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        state.photo3[i] = BufferedInputFile(
            file=image_data, filename=f"{i}21.jpg")

    """image_path = os.path.join(IMAGE_FOLDER, f"no_cabinet_photo.jpg")
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Використовуємо BufferedInputFile для байтових даних
    state.no_cabinet_photo = BufferedInputFile(
        file=image_data, filename=f"no_cabinet_photo.jpg")"""

    """response = state.supabase.table("users").insert({
        "user_id": 5842685,
        "name": 'ijhsfdkj',
        "phone": '0953342119'
    }).execute()"""

    with open(f"images/incubation.jpg", 'rb') as image_file:
        image_data = image_file.read()
    state.photo_incubation = BufferedInputFile(
        file=image_data, filename=f"incubation.jpg")
