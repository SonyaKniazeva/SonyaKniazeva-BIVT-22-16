
import vk as vk
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from bs4 import BeautifulSoup
import requests
import threading, schedule, time
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class News:
    def __init__(self, number, header, link_to):
        self.number = number
        self.header = header
        self.link_to = link_to

    def get_news(self, count_i):
        if count_i > 1:
            go_to_message = (f"\n"
                f"{self.number}) {self.header} "
                             f"{self.link_to} ")
            return go_to_message
        if count_i == 1:
            go_to_message = (f"{self.number}) {self.header} "
                             f"{self.link_to} ")
            return go_to_message



def get_last_news(count, user__id):
    if 1 <= count and count <= 10:
        request = requests.get('https://www.rbc.ru/')
        b = BeautifulSoup(request.text, "html.parser")
        head = b.select('.main__feed__title')
        result = []
        for i in range(1, count + 1):
            header_our = head[i].getText()
            link = b.select('[class *= "main__feed__link js-yandex-counter js-visited"]')[i].get(
                "href")  # [attribute*="value"]:Ищет HTML-элементы с атрибутом attribute, значение которого содержит подстроку value.

            one_new = News(i, header_our, link)
            result.append(one_new.get_news(i))
            i += 1
        return result
    else:
        return "Введите число в нужном диапазоне"

def get_news_theme(count, link_from, user__id):
    if 1 <= count and count <= 10:
        request = requests.get(link_from)
        b = BeautifulSoup(request.text, "html.parser")
        head = b.select('[class *= "item__title rm-cm-item-text js-rm-central-column-item-text"]')

        result = []
        for i in range(0, count):
            header_our = head[i].getText()
            link = b.select('.item .item__link')[i].get("href")
            one_new = News(i + 1, header_our, link)
            result.append(one_new.get_news(i + 1))
            i += 1
        return result
    else:
        return "Введите число в нужном диапазоне"

def get_news_theme_new_economy(count, user__id):
    if 1 <= count and count <= 10:
        request = requests.get('https://www.rbc.ru/neweconomy/?utm_source=topline')
        b = BeautifulSoup(request.text, "html.parser")
        head = b.select('[class *= "q-item__title js-rm-central-column-item-text"]')
        result = []
        for i in range(0, count):
            header_our = head[i].getText()[2:-1]
            link = b.select('.q-item .q-item__link')[i].get("href")
            one_new = News(i + 1, header_our, link)
            result.append(one_new.get_news(i + 1))
            i += 1
        return result
    else:
        return "Введите число в нужном диапазоне"

