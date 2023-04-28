import json
import os

import PIL
from PIL import Image
from aiogram import Bot, Dispatcher, executor, filters, types
from dotenv import load_dotenv

from main.single_index import Recognizer

load_dotenv("bot/.env")

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CONFIG_INFO_JSON = os.getenv("CONFIG_INFO_JSON")

# config
IMG_DIR = "../data/filtered/"
UPL_DIR = "bot/data/uploaded/"
TOP_K = 5

MAX_SIZE = (256, 256)

if not os.path.exists(UPL_DIR):
    os.makedirs(UPL_DIR)

config_info = None
if os.path.exists(CONFIG_INFO_JSON):
    with open(CONFIG_INFO_JSON, 'r') as fp:
        config_info = json.load(fp)

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


@dp.message_handler(filters.CommandStart())
async def send_welcome(message: types.Message):
    greeting = f"Hi, {message.from_user.first_name}!\n"
    msg_info_1 = f"Upload a picture and I will try to find {TOP_K} similar pictures from my database.\n"
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
            for idx in range(TOP_K):
                path = top_similar["paths"][idx]
                if not os.path.exists(path):
                    path = os.path.join(os.getcwd(), path)

                path = os.path.normpath(path)
                folder, file = path.split(os.sep)[-2], path.split(os.sep)[-1]
                caption = ''
                if config_info is not None:
                    info = config_info.get(folder, {}).get(file, {})
                    description = info.get("description", "")
                    if description:
                        caption += f"**{description}**\n"
                    link = info.get("href", "")
                    if link:
                        caption += f'[Link]({link})\n'
                if not caption:
                    caption += f"{folder}/{file}\n"

                caption = caption.replace('.', r'\.')
                if os.path.exists(path):
                    media.attach_photo(types.InputFile(path), caption=caption, parse_mode='MarkdownV2')
                else:
                    print(str(path), 'does not exist')

            await message.answer_media_group(media=media)
        except Exception as e:
            await message.answer("Error: \n" + str(e))

    else:
        await message.answer('You should upload photo in "jpg", "png", or "jpeg" format.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
