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


    print(state.users)


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


    with open(f"images/incubation.jpg", 'rb') as image_file:
        image_data = image_file.read()
    state.photo_incubation = BufferedInputFile(
        file=image_data, filename=f"incubation.jpg")
