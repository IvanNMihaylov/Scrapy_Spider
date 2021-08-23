import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from typing_extensions import get_args
from requests_html import HTMLSession

def getInfo(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep = 1)

    all_info = {
        'category': r.html.xpath('//*[@id="content"]/div[1]/div[1]/a[2]', first =True).text,
        'subcategory':  r.html.xpath('//*[@id="content"]/div[1]/div[1]/a[3]', first =True).text,
        'title': r.html.xpath('//*[@id="content"]/div[1]/div[2]/div[2]/h1', first =True).text,
        'subtitle': r.html.xpath('//*[@id="content"]/div[1]/div[2]/div[2]/h2', first =True).text,
        'product_number': r.html.xpath('//*[@id="content"]/div[1]/div[2]/div[2]/div[1]/div[1]/strong', first =True).text,
        'price': r.html.xpath('//*[@id="content"]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div[1]', first = True).text
    }
    return all_info

baseurl = 'https://gplay.bg/'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

productlinks = []
hardware_items = [
    'геймърски-клавиатури', 'геймърски-мишки', 'геймърски-падове-за-мишки', 'геймърски-слушалки',
    'периферия-комплекти', 'гейминг-контролери', 'аудио-системи', 'уеб-камери',
    'микрофони', 'графични-таблети', 'usb-памети', 'карти-памет', 'usb-хъбове', 'дънни-платки',
    'процесори', 'видео-карти', 'памети', 'комплекти-геймингw-хардуер', 'вътрешни-дискове', 
    'външни-дискове', 'оптични-устройства', 'захранвания', 'компютърни-кутии', 'охладители',
    'вентилатори', 'rgb-аксесоари', 'звукови-карти', 'кепчър-карти', 'контролери'
]

for hardware in hardware_items:
    for x in range(1,8):
        # I use filters on the site for available items and price index
        r = requests.get(f'https://gplay.bg/{hardware}?flag[0]=available&prices[0]=0&prices[1]=200&perPage=60&sort=price_asc&page={x}')
        soup = BeautifulSoup(r.content, 'lxml')

        productlist = soup.find_all('div', class_='product-item')

        for item in productlist:
            for link in item.find_all('a', href = True, class_='product-name'):
                productlinks.append(link['href'])

gplaylist_item = []
for link in productlinks: 
    if link.endswith('-1') or link.endswith('-2') or link.endswith('-3'):                   # this is for separate items which are the same 
        if link[:-2] in productlinks:                                                       # (for example - diferent color)
            continue
        else:
            gplaylist_item.append(getInfo(link))
    else:
        gplaylist_item.append(getInfo(link))

with open('app.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(gplaylist_item, ensure_ascii=False))                                 # add in json file

df = pd.DataFrame(gplaylist_item)
print(df.head(10))                                                                          # preview items with  data frame 