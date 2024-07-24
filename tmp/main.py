#import asyncio
#import requests
#import random
#from aiogram import Bot, Dispatcher, F
#from aiogram.filters import CommandStart, Command
#from aiogram.types import Message, FSInputFile
#from config import TOKEN, TOKEN_API
#from gtts import gTTS
#import os

# Здесь вставьте ваш API ключ от OpenWeatherMap
#WEATHER_API_KEY = TOKEN_API
#CITY_NAME = 'Москва'

#bot = Bot(token=TOKEN)
#dp = Dispatcher()

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile('TG02.pdf')
    await doc.send_document(message.chat.id, doc=doc)

@dp.message(Command('voise'))
async def voise(message: Message):
    voise = FSInputFile('WhatsApp Ptt 2024-07-20 at 16.42.37.ogg')
    await message.answer_voice(voice=voise)

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('WhatsApp Video 2024-07-10 at 21.16.35.mp4')
    await bot.send_video(message.chat.id, video=video)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('WhatsApp Audio 2024-07-10 at 21.16.35.mp3')
    await bot.send_audio(message.chat.id, audio=audio)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:1. Скручивания: 3 подхода по 15 повторений 2. Велосипед: 3 подхода по 20 повторений (каждая сторона) 3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2: 1. Подъемы ног: 3 подхода по 15 повторений 2. Русский твист: 3 подхода по 20 повторений (каждая сторона) 3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3: 1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений 2. Горизонтальные ножницы: 3 подхода по 20 повторений 3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
    rand_tr = random.choice(training_list)
    await message.answer(f'Это ваша мини-тренировка на сегодня {rand_tr}')
    tts = gTTS(text=rand_tr, lang='ru')
    tts.save('training.ogg')
    audio = FSInputFile('training.ogg')
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
    os.remove('training.ogg')

def get_weather(city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        weather_info = f'Погода в {city_name}:\nТемпература: {temperature}°C\nОписание: {weather_description}'
        return weather_info
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            return 'Ошибка авторизации: проверьте ваш API ключ.'
        return f'HTTP ошибка: {http_err}'
    except requests.exceptions.ConnectionError as conn_err:
        return f'Ошибка соединения: {conn_err}'
    except requests.exceptions.Timeout as timeout_err:
        return f'Ошибка времени ожидания: {timeout_err}'
    except requests.exceptions.RequestException as req_err:
        return f'Ошибка запроса: {req_err}'
    except Exception as e:
        return f'Не удалось получить данные о погоде: {e}'

@dp.message(Command('weather'))
async def weather(message: Message):
    weather_info = get_weather(CITY_NAME)
    await message.answer(weather_info)

@dp.message(Command('photo'))
async def photo(message: Message):
    list = [
        'https://4x4photo.ru/wp-content/uploads/2023/05/85c5efe1-8e0b-40a5-bac7-57dce7d9e3a7.jpg',
        'https://coolsen.ru/wp-content/uploads/2021/11/134-20211129_204337.jpg',
        'https://wallbox.ru/wallpapers/main2/201728/14998384635965b7ffade143.60855190.jpg'
    ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка!')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого! Какая фотка!', 'Красота неземная!', 'Прикольная фоточка!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg ')

@dp.message(F.text == 'Что такое ИИ?')
async def aitext(message: Message):
    await message.answer('Искусственный интеллект(ИИ) — это комплекс методик компьютерных наук, а также математики, биологии и психологии, которые занимаются разработкой систем, способных выполнять задачи, обычно требующие человеческого интеллекта.')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n/start \n/help\n/weather\n/photo')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

@dp.message()
async def start(message: Message):
    if message.text.lower() == 'тест':
        await message.answer('Тест пройден!')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

