import asyncio
import os
import aiofiles
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import File as AiogramFile
from aiogram.types import FSInputFile
import requests
from config import TOKEN1

# Создаем папку для сохранения изображений, если ее нет
if not os.path.exists('img'):
    os.makedirs('img')

bot = Bot(token=TOKEN1)
dp = Dispatcher()

async def download_photo(file_id, file_name):
    file: AiogramFile = await bot.get_file(file_id)
    file_path = file.file_path
    destination = f'img/{file_name}'
    await bot.download_file(file_path, destination)

@dp.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id
    file_name = f"{file_id}.jpg"

    await download_photo(file_id, file_name)
    await message.answer(f'Фото сохранено как {file_name}')

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("WhatsApp Ptt 2024-07-20 at 16.42.37.ogg")
    await message.answer_voice(voice)

def translate_text_to_english(text):
    url = "https://api.mymemory.translated.net/get"
    params = {
        'q': text,
        'langpair': 'ru|en'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200 and 'responseData' in data:
        return data['responseData']['translatedText']
    else:
        return 'Не удалось выполнить перевод'

@dp.message(F.text)
async def handle_text(message: Message):
    text_to_translate = message.text
    translated_text = translate_text_to_english(text_to_translate)
    await message.answer(f'Перевод: {translated_text}')
@dp.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет! Отправь мне фото, и я сохраню его. Или отправь мне любой текст, и я переведу его на английский язык.")
@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет сохранять фотографии и переводит любой текст, который вы отправляете, на английский язык.")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
