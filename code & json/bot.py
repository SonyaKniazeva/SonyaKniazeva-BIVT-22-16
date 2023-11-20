from __future__ import annotations

from pydoc import html
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config
# from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
import asyncio
from datetime import datetime

import random
import json

bot = Bot(token = config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)

dp = Dispatcher(storage=storage)

class FSMtrips(StatesGroup):
    get_random_trip = State()

@dp.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    itembtn1 = types.KeyboardButton(text = 'Место дня')
    itembtn2 = types.KeyboardButton(text = 'Случайное путешествие по России')
    itembtn3 = types.KeyboardButton(text ='Случайный лайфхак для путешественников')
    itembtn4 = types.KeyboardButton(text = 'Отмена')
    kb = [[itembtn1], [itembtn2], [itembtn3], [itembtn4]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Что хотите получить?', reply_markup=keyboard)
    #await state.set_state(default_state)


# bot.remove_webhook()
# bot.set_webhook("https://functions.yandexcloud.net/d4e54h896vjvu0dda61d")

def get_info_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

@dp.message(F.text == "Место дня", StateFilter(default_state))
async def send_place(message: types.Message, state: FSMContext):
    day = datetime.today().day
    number = day % 10
    data = get_info_from_json('place_day.json')
    tmp = data.get(str(number))
        # photo = 'https://storage.yandexcloud.net/picture-places/' + str(number) + '.jpg'
    await message.answer(tmp)
    await state.clear()
        # bot.send_photo(message.chat.id, photo)


@dp.message(F.text == "Случайное путешествие по России", StateFilter(default_state))
async def choose_type_of_trips(message: types.Message, state: FSMContext):
    kb = [[types.KeyboardButton(text = 'Готовый план путешествия')], [types.KeyboardButton(text = 'Гайд по городу')], [types.KeyboardButton(text = 'Отмена')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Выберите формат', reply_markup=keyboard)
    await state.set_state(FSMtrips.get_random_trip)

@dp.message(F.text == "Готовый план путешествия", FSMtrips.get_random_trip)
async def send_place(message: types.Message, state: FSMContext):
    number = random.randint(1, 10)
    data = get_info_from_json('planned_trips.json')
    tmp = data.get(str(number))
    city, link = tmp.split(' = ')
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=city, url=link))
    await message.answer('Перейдите по ссылке ниже:', reply_markup=builder.as_markup())
    await state.set_state(FSMtrips.get_random_trip)
@dp.message(F.text == "Гайд по городу", FSMtrips.get_random_trip)
async def send_place(message: types.Message, state: FSMContext):
    number = random.randint(1, 18)
    data = get_info_from_json('unplanned_trips.json')
    tmp = data.get(str(number))
    city, link = tmp.split(' = ')
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=city, url=link))
    await message.answer('Перейдите по ссылке ниже:', reply_markup=builder.as_markup())
    await state.set_state(FSMtrips.get_random_trip)


@dp.message(F.text == "Случайный лайфхак для путешественников", StateFilter(default_state))
async def send_place(message: types.Message, state: FSMContext):
    number = random.randint(1, 29)
    data = get_info_from_json('lifehacks.json')
    tmp = data.get(str(number))
    name, link = tmp.split(' = ')
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=name, url=link))
    await message.answer('Перейдите по ссылке ниже:', reply_markup=builder.as_markup())
    await state.clear()

# default_state - это то же самое, что и StateFilter(None)
@dp.message(StateFilter(default_state), Command("cancel"))
@dp.message(StateFilter(default_state), F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: types.Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Нечего отменять, нажмите команду /start",
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message(Command('cancel'), FSMtrips.get_random_trip)
@dp.message(F.text.lower() == "отмена")
async def process_cancel_state(message: types.Message, state: FSMContext):
    itembtn1 = types.KeyboardButton(text='Место дня')
    itembtn2 = types.KeyboardButton(text='Случайное путешествие по России')
    itembtn3 = types.KeyboardButton(text='Случайный лайфхак для путешественников')
    itembtn4 = types.KeyboardButton(text='Отмена')
    kb = [[itembtn1], [itembtn2], [itembtn3], [itembtn4]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text='Нажмите на одну из кнопок', reply_markup=keyboard)
    await state.clear()
    # await state.set_state(default_state)

@dp.message(Command('cancel'), ~StateFilter(default_state, FSMtrips.get_random_trip))
@dp.message(F.text.lower() == "отмена")
async def process_cancel_state(message: types.Message, state: FSMContext):
    await message.answer(text='Возвращаемся в начало', reply_markup=types.ReplyKeyboardRemove())
    await state.clear()

@dp.message(StateFilter(default_state))
async def send_echo(message: types.Message):
    await message.answer('Извините, такой команды нет\nДля возвращения в начало нажмите /start')

@dp.message(FSMtrips.get_random_trip)
async def send_echo(message: types.Message):
    await message.answer('Извините, такой команды нет\nДля продолжения нажмите одну из кнопок\nДля возвращения в начало нажмите /start\nДля отмены нажмите /cancel')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())