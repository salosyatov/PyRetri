import base64
import os
from pathlib import Path

import PIL
import requests
from PIL import Image
from aiogram import Bot, Dispatcher, executor, filters, types

from dotenv import load_dotenv

from main.single_index import Recognizer

load_dotenv("bot/.env")

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# config
IMG_DIR = "../data/filtered/"                    # common data for all services
UPL_DIR = "bot/data/uploaded/"  # upload dir just for web part
TOP_K = 5                                        # api service provide top 5 now
API_ENDPOINT = os.getenv("API_ENDPOINT_LOCAL")   # local api for testing
MAX_SIZE = (256, 256)


if not os.path.exists(UPL_DIR):
    os.makedirs(UPL_DIR)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_image(path, resize=True):
    image = Image.open(path).convert("RGB")
    if resize:
        image = image.resize(MAX_SIZE, Image.Resampling.BILINEAR)
    return image


def get_top_similar(image):
    recognizer = Recognizer()
    paths, names = recognizer.find_similar(image, k=TOP_K)
    top_similar = {"paths": paths, "labels": names}
    return top_similar


def get_top_similar_from_file(path):
    image = PIL.Image.open(path).convert("RGB")
    top_similar = get_top_similar(image)
    return top_similar

    with open(path, 'rb') as f:
        im_b64 = base64.b64encode(f.read())

    data = {'image': im_b64}
    response = requests.post(url=API_ENDPOINT, data=data, timeout=30, verify=False)

    top_similar = response.json()
    return top_similar


@dp.message_handler(filters.CommandStart())
async def send_welcome(message: types.Message):
    greeting = f"Hi, {message.from_user.first_name}!\n"
    msg_info_1 = f"Upload a picture and I will try to find 5 similar pictures from my database.\n"
    await message.reply(greeting + msg_info_1)


@dp.message_handler(content_types=['photo', 'document'])
async def get_landmarks(message: types.Message):

    if message.photo:
        PhotoSize = message.photo[-1]
        file_info = await bot.get_file(PhotoSize.file_id)
    elif message.document:
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)

    if file_info.file_path.lower().endswith(('.png', '.jpg', '.jpeg')):

        await message.reply("Just a second...")

        save_path = UPL_DIR + file_info.file_path

        if message.photo:
            await PhotoSize.download(destination_dir=UPL_DIR)
        elif message.document:
            await bot.download_file(file_info.file_path, save_path)

        try:
            top_similar = get_top_similar_from_file(save_path)

            # Good bots should send chat actions...
            await types.ChatActions.upload_photo()

            media = types.MediaGroup()
            paths = []
            for idx in range(TOP_K):
                path = top_similar["paths"][idx]
                if not Path(path).exists():
                    path = os.path.join(os.getcwd(), path)

                path = str(Path(path).resolve())
                path = path.replace("/", os.sep).replace("\\", os.sep)
                name = Path(path).stem
                if os.path.exists(path):
                    media.attach_photo(types.InputFile(path), name.replace("_", " "))
                else:
                    print(str(path), 'does not exist')

                paths.append(str(path))

            await message.answer_media_group(media=media)
        except Exception as e:
            await message.answer("Error: \n" + str(e))

    else:
        await message.answer('You should upload photo in "jpg", "png", or "jpeg" format.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
