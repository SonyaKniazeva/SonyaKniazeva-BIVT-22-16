import vk as vk
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from bs4 import BeautifulSoup
import requests
import threading, schedule, time
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from functions import *

group_key = 'vk1.a.m-cM02flMKFt8-vcY4heTBHXupBH10tZFI2VF4AZvs_mrrCYoabPoK80MQfxQsHSN-cQgoUmAw5gSOMFbLglneo9CSyPjGgpG4hW4qLxtVEGuIeK2TUoi379dFhAVi3X_pruMAyO2b0y6e5FuD1I-vJbgvSq2A6381DChkyZ1sbsffcNKuk9QgPXBcEUEYlKquNfnJowHz4U848Ccd5yBA'

#ССЫЛКА НА СООБЩЕСТВО МОЕГО БОТА: https://vk.com/public222798457

def notif_thread():
    while True:
        schedule.run_pending()
        time.sleep(60)


threading.Thread(target=notif_thread).start()


def _check_time(message: list):
    num1 = int(message[0])
    num2 = int(message[1])
    if 0 <= num1 <= 23 and 0 <= num2 <= 59:
        return True
    return False

def get_last_news_for_shedule(n, user_id_id):
        vk.messages.send(user_id= user_id_id,
            random_id=get_random_id(),
            message=get_last_news(n, user_id_id))

class Users:
    def __init__(self, user_id):
        self.user_id = user_id
    uved_count = 1
    news = -1
    # 1-последние, 2-по теме, -1-дефолт
    last_request = 'smth'



keyboard_start = VkKeyboard(one_time = True)
keyboard_start.add_button('В начало', color = VkKeyboardColor.POSITIVE)

keyboard0 = VkKeyboard(one_time = True)
keyboard0.add_button('Сейчас получить новости', color = VkKeyboardColor.PRIMARY)
keyboard0.add_line()
keyboard0.add_button('Настроить автоматическое получение', color = VkKeyboardColor.PRIMARY)
keyboard0.add_line()
keyboard0.add_button('В начало', color = VkKeyboardColor.NEGATIVE)

keyboard1 = VkKeyboard(one_time = True)
keyboard1.add_button('Последние новости', color = VkKeyboardColor.PRIMARY)
keyboard1.add_button('Новости по теме', color = VkKeyboardColor.PRIMARY)
keyboard1.add_line()
keyboard1.add_button('В начало', color = VkKeyboardColor.NEGATIVE)

keyboard2 = VkKeyboard(one_time = True)
keyboard2.add_button('Москва', color = VkKeyboardColor.PRIMARY)
keyboard2.add_button('Новая экономика', color = VkKeyboardColor.PRIMARY)
keyboard2.add_line()
keyboard2.add_button('Спорт', color = VkKeyboardColor.PRIMARY)
keyboard2.add_button('Новости технологий и медиа', color = VkKeyboardColor.PRIMARY)
keyboard2.add_line()
keyboard2.add_button('В начало', color = VkKeyboardColor.NEGATIVE)

vk_session = vk_api.VkApi(token = group_key)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

users_dict = {}

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.user_id in users_dict:

            if (event.text.startswith('Привет')
                    or event.text.startswith('привет')
                    or event.text.startswith('В начало')):
                vk.messages.send(keyboard=keyboard0.get_keyboard(),
                                 key=(
                                     "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                 server=("https://lp.vk.com/whp/222798457"),
                                 ts=("29"),
                                 user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message='Готов присылать последние новости хоть сейчас, хоть каждый день - когда душе будет угодно!')

            elif event.text.startswith('Сейчас получить новости'):
                vk.messages.send(keyboard=keyboard1.get_keyboard(),
                                 key=(
                                     "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                 server=("https://lp.vk.com/whp/222798457"),
                                 ts=("29"),
                                 user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message='Хотите все последние новости или только по конкретной теме?')

            elif event.text.startswith('Последние новости'):
                users_dict[event.user_id].news = 1
                vk.messages.send(user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message='Введите количество новостей 1-10')

            elif event.text.isdigit():

                    if (users_dict[event.user_id].news == 1):
                        if get_last_news(int(event.text), event.user_id) != "Введите число в нужном диапазоне":
                            vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                                             key=(
                                                 "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                             server=("https://lp.vk.com/whp/222798457"),
                                             ts=("29"),
                                             user_id=event.user_id,
                                             random_id=get_random_id(),
                                             message=get_last_news(int(event.text), event.user_id))
                            users_dict[event.user_id].news = 0
                        else:
                            vk.messages.send(user_id=event.user_id,
                                             random_id=get_random_id(),
                                             message=get_last_news(int(event.text), event.user_id))

                    elif (users_dict[event.user_id].news == 2):
                         if users_dict[event.user_id].last_request == 'Москва':
                             if get_news_theme(int(event.text), 'https://www.rbc.ru/gorod/?utm_source=top', event.user_id) != "Введите число в нужном диапазоне":
                                 users_dict[event.user_id].news = 0
                                 vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                                                  key=(
                                                      "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                                  server=("https://lp.vk.com/whp/222798457"),
                                                  ts=("29"),
                                                  user_id=event.user_id,
                                                  random_id=get_random_id(),
                                                  message=get_news_theme(int(event.text),
                                                                         'https://www.rbc.ru/gorod/?utm_source=top',
                                                                         event.user_id))
                             else:
                                 vk.messages.send(user_id=event.user_id,
                                                  random_id=get_random_id(),
                                                  message=get_news_theme(int(event.text),
                                                                         'https://www.rbc.ru/gorod/?utm_source=top',
                                                                         event.user_id))
                         if users_dict[event.user_id].last_request == 'Новая экономика':
                             if get_news_theme_new_economy(int(event.text), event.user_id)!= "Введите число в нужном диапазоне":
                                 users_dict[event.user_id].news = 0
                                 vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                                                  key=(
                                                      "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                                  server=("https://lp.vk.com/whp/222798457"),
                                                  ts=("29"),
                                                  user_id=event.user_id,
                                                  random_id=get_random_id(),
                                                  message=get_news_theme_new_economy(int(event.text), event.user_id))
                             else:
                                 vk.messages.send(user_id=event.user_id,
                                                  random_id=get_random_id(),
                                                  message=get_news_theme_new_economy(int(event.text), event.user_id))
                         if users_dict[event.user_id].last_request == 'Спорт':
                             if get_news_theme(int(event.text), 'https://sportrbc.ru/?utm_source=topline', event.user_id) != "Введите число в нужном диапазоне":
                                 users_dict[event.user_id].news = 0
                                 vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                                                  key=(
                                                      "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                                  server=("https://lp.vk.com/whp/222798457"),
                                                  ts=("29"),
                                                  user_id=event.user_id,
                                                  random_id=get_random_id(),
                                                  message=get_news_theme(int(event.text),
                                                                         'https://sportrbc.ru/?utm_source=topline',
                                                                         event.user_id))
                             else:
                                 vk.messages.send(user_id=event.user_id,
                                                  random_id=get_random_id(),
                                                  message=get_news_theme(int(event.text),
                                                                         'https://sportrbc.ru/?utm_source=topline',
                                                                         event.user_id))

                         if users_dict[event.user_id].last_request == 'Новости технологий и медиа':
                             if get_news_theme(int(event.text), 'https://www.rbc.ru/technology_and_media/?utm_source=topline', event.user_id) != "Введите число в нужном диапазоне":
                                 users_dict[event.user_id].news = 0
                                 vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                                                  key=(
                                                      "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                                  server=("https://lp.vk.com/whp/222798457"),
                                                  ts=("29"),
                                                  user_id=event.user_id,
                                                  random_id=get_random_id(),
                                                  message=get_news_theme(int(event.text),
                                                                         'https://www.rbc.ru/technology_and_media/?utm_source=topline',
                                                                         event.user_id))
                             else:
                                 vk.messages.send(user_id=event.user_id,
                                                  random_id=get_random_id(),
                                                  message=get_news_theme(int(event.text),
                                                                         'https://www.rbc.ru/technology_and_media/?utm_source=topline',
                                                                         event.user_id))

                    else:
                        vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                                         key=(
                                             "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                         server=("https://lp.vk.com/whp/222798457"),
                                         ts=("29"),
                                         user_id=event.user_id,
                                         random_id=get_random_id(),
                                         message='Нажмите на кнопку')

            elif event.text.startswith('Новости по теме'):
                users_dict[event.user_id].news = 2
                vk.messages.send(keyboard=keyboard2.get_keyboard(),
                                 key=(
                                     "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                 server=("https://lp.vk.com/whp/222798457"),
                                 ts=("29"),
                                 user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message='Выберите тему новостей')

            elif event.text.startswith('Москва'):
                users_dict[event.user_id].last_request = 'Москва'
                vk.messages.send(user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message='Введите количество новостей 1-10')

            elif event.text.startswith('Новая экономика'):
                users_dict[event.user_id].last_request = 'Новая экономика'
                vk.messages.send(user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message='Введите количество новостей 1-10')

            elif event.text.startswith('Спорт'):
                users_dict[event.user_id].last_request = 'Спорт'
                vk.messages.send(user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message='Введите количество новостей 1-10')

            elif event.text.startswith('Новости технологий и медиа'):
                users_dict[event.user_id].last_request = 'Новости технологий и медиа'
                vk.messages.send(user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message='Введите количество новостей 1-10')

            elif event.text.startswith('Настроить автоматическое получение'):
                users_dict[event.user_id].last_request = 'Настроить автоматическое получение'
                vk.messages.send(user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message=f'Введите время в формате hh:mm:количество новостей(1-10), пример -> 08:00:10 -> так будете получать уведомление каждый день в 08:00, которое будет содержать 10 последних новостей')

            elif users_dict[event.user_id].last_request == 'Настроить автоматическое получение':
                message = event.text
                message_list = message.strip(' ').split(':')
                # если все ок добавляем
                if (len(message_list) == 3 and len(message_list[0]) == len(message_list[1]) == 2 and 1 <= len(
                        message_list[2]) <= 2 and _check_time(message_list)):
                    users_dict[event.user_id].uved_count = int(message_list[2])
                    # включение уведомлений конкретному пользователю
                    schedule.every().day.at(message[0:5]).do(get_last_news_for_shedule,
                                                             users_dict[event.user_id].uved_count, event.user_id)
                    vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                                     key=(

                                         "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                     server=("https://lp.vk.com/whp/222798457"),
                                     ts=("29"),
                                     user_id=event.user_id,
                                     random_id=get_random_id(),
                                     message='Уведомления успешно включены')

                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message="Неверный формат ввода")
                    vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                                     key=(
                                         "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                     server=("https://lp.vk.com/whp/222798457"),
                                     ts=("29"),
                                     user_id=event.user_id,
                                     random_id=get_random_id(),
                                     message='Нажмите на кнопку')

            else:
                vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                                 key=(
                                     "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                                 server=("https://lp.vk.com/whp/222798457"),
                                 ts=("29"),
                                 user_id=event.user_id,
                                 random_id=get_random_id(),
                                 message='Нажмите на кнопку')

        else:
            users_dict[event.user_id] = Users(event.user_id)
            vk.messages.send(keyboard=keyboard_start.get_keyboard(),
                             key=(
                                 "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJxdWV1ZV9pZCI6IjIyMjc5ODQ1NyIsInVudGlsIjoxNjk2MzQwMDg5OTExMDIwMjMzfQ.cTxY-B5WHahMLY7UQvWm7R74kbgiJhw4fdMcMej8IYnYmICeNyGhMn8TmMHXYVpcZlf_BwJCiWDuP_bt51uVDA"),
                             server=("https://lp.vk.com/whp/222798457"),
                             ts=("29"),
                             user_id=event.user_id,
                             random_id=get_random_id(),
                             message='Нажмите на кнопку')