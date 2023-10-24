import requests
from bs4 import BeautifulSoup
import json

def get_text(url):
#из URL вытаскиваем html
    r = requests.get(url)
    text=r.text
    return text

my_url = 'https://www.onetwotrip.com/ru/blog/smart-travel/life-hack/7-tips-for-safe-travel/'

def get_advice(text, number):
    request = requests.get(my_url)
    b = BeautifulSoup(request.text, "html.parser")
    head = b.select('[id]:is(span)')[number - 1].getText()
    number += number - 1
    advice_text = str(b.select('h2 ~ p')[number - 1])
    if number != 7:
        final_text = advice_text[3:-4]
    else:
        tmp = advice_text[3:-4]
        final_text = tmp[:-144]
    return (f"{head[3:]}: "
            f"{final_text}")

dict_with_advice = {}
for num in range(1, 8):
    getting = get_advice(get_text(my_url), num)
    dict_with_advice[num] = getting
print(dict_with_advice)

with open('advice.json', 'w', encoding = 'utf-8') as file:
    tmp = json.dumps(dict_with_advice, ensure_ascii=False,  indent=4)
    file.write(tmp)

