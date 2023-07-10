from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import NetworkError
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bs4 import BeautifulSoup
from random import randint
import requests
import sqlite3
from django.conf import settings
import telegram
from datetime import date

hello = """Hello! You are using the "Arbitration Goose" command bot.

✅ In this bot, you can get a photo to pass the checkpoint.

Brief instructions:
1. Click the "👨 Get a photo to pass the checkpoint" button.
2. Refresh the photo until you get the desired face.
3. Download the file to your device.
4. Upload the file from your device to Tsuker's account (Facebook).

❗️Attention
You need to upload the photo from your device, don't upload it directly from Telegram to Facebook, as the photo won't pass the checkpoint."""

chat = """❤️ And don't forget to join our chat, where we share up-to-date information about FB uploads, tricks, and much more."""

TOKEN = 'ENTER BOT TOKEN HERE'

admins = [242494911, 689892377, 983265598]

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

connect = sqlite3.connect('admin.db')
cursor = connect.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id text, joining_date text)")
connect.commit()


class States(StatesGroup):
    text = State()


from datetime import date

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        if cursor.execute(f"SELECT * FROM users WHERE id='{message.chat.id}'").fetchone() is None:
            
            joining_date_text = date.today().strftime('%Y-%m-%d')
            print(joining_date_text)
            cursor.execute(f"INSERT INTO users (id, joining_date) VALUES ('{message.chat.id}', '{joining_date_text}')")
            connect.commit()
          
        keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton('👨Получить фото для прохода чекпоинта')]],
                                             resize_keyboard=True)
        await bot.send_message(message.chat.id, hello, reply_markup=keyboard)
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('📣Наш ЧАТ', url='https://t.me/arbi_goose_chat'))
        await bot.send_message(message.chat.id, chat, reply_markup=keyboard)

    except Exception as e:
        print(f"Error inserting data into users table: {str(e)}")


@dp.message_handler(commands=['message'])
async def sending(message: types.Message):
    if message.chat.id in admins:
        await bot.send_message(message.chat.id, 'Введите сообщение, которое хотите отправить пользователям')
        await States.text.set()
    else:
        keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton('👨Получить фото для прохода чекпоинта')]],
                                             resize_keyboard=True)
        await bot.send_message(message.chat.id, hello, reply_markup=keyboard)
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('📣Наш ЧАТ', url='https://t.me/arbi_goose_chat'))
        await bot.send_message(message.chat.id, chat, reply_markup=keyboard)


@dp.message_handler(state=States.text, content_types=['text'])
async def end_sending(message: types.Message, state: FSMContext):
    await state.finish()
    for users in cursor.execute(f"SELECT * FROM users WHERE id!='{message.chat.id}'").fetchall():
        try:
            keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton('👨Получить фото для прохода чекпоинта')]],
                                                 resize_keyboard=True)
            await bot.send_message(users[0], 'Сообщение от администратора:\n\n' + message.text, reply_markup=keyboard)
        except:
            pass
    await bot.send_message(message.chat.id, 'Сообщение отправлено', reply_markup=keyboard)


@dp.message_handler()
async def else_messages(message: types.Message):
    if message.text in ['👨Получить фото для прохода чекпоинта', '🔄Обновить']:
        with requests.Session() as session:
            site = session.get('https://this-person-does-not-exist.com')
            parser = BeautifulSoup(site.text, 'html.parser')
            data = session.get('https://this-person-does-not-exist.com'+parser.find('img', id='avatar')['src'])
            print('https://this-person-does-not-exist.com'+parser.find('img', id='avatar')['src'])
            photo = (f'image{randint(1000, 9999)}.jpeg', data.content)
        keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton('🔄Обновить')]], resize_keyboard=True)
        await bot.send_document(message.chat.id, photo, reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup([[types.KeyboardButton('👨Получить фото для прохода чекпоинта')]],
                                             resize_keyboard=True)
        await bot.send_message(message.chat.id, hello, reply_markup=keyboard)
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('📣Наш ЧАТ', url='https://t.me/arbi_goose_chat'))
        await bot.send_message(message.chat.id, chat, reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
