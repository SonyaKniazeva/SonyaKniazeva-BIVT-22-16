from pydoc import html
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
import asyncio
from datetime import datetime

import random
import json

bot = Bot(token = config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
dp = Dispatcher()
# dp['today_is'] = datetime.date().day
storage = MemoryStorage()

class FSMtrips(StatesGroup):
    get_random_trip = State()

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    itembtn1 = types.KeyboardButton(text = 'Место дня')
    itembtn2 = types.KeyboardButton(text = 'Случайное путешествие')
    itembtn3 = types.KeyboardButton(text ='Лайфхаки для путешественников')
    kb = [[itembtn1], [itembtn2], [itembtn3]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Что хотите получить?', reply_markup=keyboard)


# bot.remove_webhook()
# bot.set_webhook("https://functions.yandexcloud.net/d4e54h896vjvu0dda61d")

def get_info_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

@dp.message(F.text == "Место дня", StateFilter(default_state))
async def send_place(message: types.Message, state: FSMContext):
    day = datetime.today().day
    # if right_day(day):
    number = day % 10
    data = get_info_from_json('place_day.json')
    tmp = data.get(str(number))
        # photo = 'https://storage.yandexcloud.net/picture-places/' + str(number) + '.jpg'
    await message.answer(tmp)
        # bot.send_photo(message.chat.id, photo)
    # else:
    #     msg = bot.send_message(message.chat.id, "Пожалуйста, введите число 1-31")
    #     bot.register_next_step_handler(msg, send_place)


@dp.message(F.text == "Случайное путешествие", StateFilter(default_state))
async def choose_type_of_trips(message: types.Message, state: FSMContext):
    kb = [[types.KeyboardButton(text = 'Готовый план')], [types.KeyboardButton(text = 'Идеи для вдохновения')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Выберите формат', reply_markup=keyboard)

async def send_place(message: types.Message, state: FSMContext):
    number = random.randint(1, 10)
    data = get_info_from_json('planned_trips.json')
    tmp = data.get(str(number))
        # photo = 'https://storage.yandexcloud.net/picture-places/' + str(number) + '.jpg'
    await message.answer(tmp)

# def send_meme(message):
#     photo = 'URL' + str(random.randint(1,5))+'.jpeg' # добавьте полученную выше ссылку бакета
#     bot.send_photo(message.chat.id, photo, reply_markup=keyboard_continue)


# @bot.message_handler(regexp="Случайное путешествие")
# def send_advice(message):
#     number = random.randint(1, 10)
#     ready_trip = get_info_from_bucket('planned_trips.json')
#     tmp = ready_trip.get(str(number))
#     bot.send_message(message.chat.id, tmp)
#
#
# @bot.message_handler(regexp="Совет по путешествиям")
# def send_advice(message):
#     number = random.randint(1, 7)
#     ready_advice = get_info_from_bucket('advice.json')
#     adv = ready_advice.get(str(number))
#     bot.send_message(message.chat.id, adv)

# @bot.message_handler(content_types=["text"])
# def handle_other_messages(message):
#     bot.send_message(message.chat.id, "Я тебя не понимаю. Нажмите на одну из кнопок.")
#
# def handler(event, context):
#     body = json.loads(event['body'])
#     update = telebot.types.Update.de_json(body)
#     bot.process_new_updates([update])
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Success')
#     }

#bot.polling(none_stop=True)
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())