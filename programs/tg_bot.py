import telebot

from telebot import types
from bot_token import token

import requests
import random
import json

bot = telebot.TeleBot(token)

BUCKET_NAME = 'trip'

def get_info_from_bucket(filename):
    url = f"https://storage.yandexcloud.net/{BUCKET_NAME}/{filename}"
    response = requests.get(url)
    return response.json()

@bot.message_handler(commands=['start'])
def send_keyboard(message, text="Что хотите получить?"):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Место дня')
    itembtn2 = types.KeyboardButton('Случайное путешествие')
    itembtn3 = types.KeyboardButton('Совет по путешествиям')
    keyboard.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.from_user.id,
                           text=text, reply_markup=keyboard)



bot.remove_webhook()
bot.set_webhook("https://functions.yandexcloud.net/d4e54h896vjvu0dda61d")

def right_day(number):
    if (1 <= number <= 31):
        return True
    return False

@bot.message_handler(regexp="Место дня")
def get_day(message):
    msg = bot.send_message(message.chat.id, "Какое сегодня число?")
    bot.register_next_step_handler(msg, send_place)

def send_place(message):
    day = int(message.text)
    if right_day(day):
        number = day % 10
        ready_place = get_info_from_bucket('place_day.json')
        tmp = ready_place.get(str(number))
        photo = 'https://storage.yandexcloud.net/picture-places/' + str(number) + '.jpg'
        bot.send_message(message.chat.id, tmp)
        bot.send_photo(message.chat.id, photo)
    else:
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите число 1-31")
        bot.register_next_step_handler(msg, send_place)


def send_meme(message):
    photo = 'URL' + str(random.randint(1,5))+'.jpeg' # добавьте полученную выше ссылку бакета
    bot.send_photo(message.chat.id, photo, reply_markup=keyboard_continue)


@bot.message_handler(regexp="Случайное путешествие")
def send_advice(message):
    number = random.randint(1, 10)
    ready_trip = get_info_from_bucket('trips.json')
    tmp = ready_trip.get(str(number))
    bot.send_message(message.chat.id, tmp)


@bot.message_handler(regexp="Совет по путешествиям")
def send_advice(message):
    number = random.randint(1, 7)
    ready_advice = get_info_from_bucket('advice.json')
    adv = ready_advice.get(str(number))
    bot.send_message(message.chat.id, adv)

@bot.message_handler(content_types=["text"])
def handle_other_messages(message):
    bot.send_message(message.chat.id, "Я тебя не понимаю. Нажмите на одну из кнопок.")

def handler(event, context):
    body = json.loads(event['body'])
    update = telebot.types.Update.de_json(body)
    bot.process_new_updates([update])
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }

#bot.polling(none_stop=True)
