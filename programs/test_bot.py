import pytest

from functions import get_last_news, get_news_theme_new_economy
from functions import get_news_theme

my_id = 323270156

def test_1_negative_input_into_last_news():
    get_last_news(-1, my_id)
    assert "Введите число в нужном диапазоне"#1-10

def test_2_big_input_into_last_news():
    get_last_news(1000, my_id)
    assert "Введите число в нужном диапазоне" #1-10

def test_3_zero_input_into_last_news():
    get_last_news(0, my_id)
    assert "Введите число в нужном диапазоне" #1-10

def test_4_correct_input_into_last_news():
    news = get_last_news(5, my_id)
    assert news != "Введите число в нужном диапазоне" #1-10


link_from = 'https://www.rbc.ru/gorod/?utm_source=top'

def test_5_negative_input_into_theme_news():
    get_news_theme(-1, link_from, my_id)
    assert "Введите число в нужном диапазоне"#1-10

def test_6_big_input_into_theme_news():
    get_news_theme(1000, link_from, my_id)
    assert "Введите число в нужном диапазоне" #1-10

def test_7_zero_input_into_theme_news():
    get_news_theme(0, link_from, my_id)
    assert "Введите число в нужном диапазоне" #1-10

def test_8_correct_input_into_theme_news():
    news = get_news_theme(5, link_from, my_id)
    assert news != "Введите число в нужном диапазоне" #1-10


def test_9_negative_input_into_theme_news_new_economy():
    get_news_theme_new_economy(-1, my_id)
    assert "Введите число в нужном диапазоне"#1-10

def test_10_big_input_into_theme_news_new_economy():
    get_news_theme_new_economy(1000, my_id)
    assert "Введите число в нужном диапазоне" #1-10

def test_11_zero_input_into_theme_news_new_economy():
    get_news_theme_new_economy(0, my_id)
    assert "Введите число в нужном диапазоне" #1-10

def test_12_correct_input_into_theme_news_new_economy():
    news = get_news_theme_new_economy(5, my_id)
    assert news != "Введите число в нужном диапазоне" #1-10