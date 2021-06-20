import requests
from bs4 import BeautifulSoup
import sqlite3

base_site = 'https://ru.iherb.com/c/vitamin-e?noi=48'
base_site = 'https://ru.iherb.com/c/vitamin-e?noi=48&p=2'
base_site = 'https://ru.iherb.com/c/Vitamin-K?noi=48'

conn = sqlite3.connect('/home/vitt/Документы/iherb.db')
cursor = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}

def parse(site):
    html = requests.get(site, headers=headers)
    bsObj = BeautifulSoup(html.content, "lxml")
    elements = bsObj.find_all('div', class_='product-cell-container col-xs-12 col-sm-12 col-md-8 col-lg-6')
    print(len(elements))
    data = []
    for element in elements:
        line = dict()
        elem = element.find('a', class_='absolute-link product-link')
        href = elem.get('href')
        img = element.find('span', class_='product-image')
        img = img.contents[1]
        img_res = img.get('src')
        if not img_res:
            img_res = img.get('data-image-src')

        try:
            rating = element.find('a', class_='rating-count').get('title')
        except AttributeError:
            rating = '0/5 - 0 Отзывы'
        rating, callback = rating.split('/5 - ')
        callback = callback.replace(' Отзывы', '')
        try:
            price = element.find('span', class_='price').text
            price = price.replace('\n', '').replace('₽', '').replace(',', '')
            price = float(price)
        except:
            price = -1.0
        callback = int(callback)
        rating = float(rating)

        line['href'] = href
        line['img'] = img_res
        line['rating'] = rating
        line['price'] = price
        line['callback'] = callback
        # print(img_res)
        data.append(line)
    return data

res_data = []
for i in range(1, 2):
    print(i)
    site = base_site + str(i)
    res_data += parse(site)
# res_data += parse(base_site_p2)
# print(len(res_data))
# for line in res_data:
#     print(line)


def sql_log(text):
    with open('sql.txt', 'wt') as f:
        f.write(text)


def put_into_sql(data):
    for line in data:
        sql = """INSERT INTO vitamins VALUES ("""
        sql += "'vitamin_k', '" + line['href'] + "', '" + line['img'] + "', " + str(line['rating']) + \
            ', ' + str(line['callback']) + ', ' + str(line['price']) + ')'
        sql_log(sql)
        cursor.execute(sql)
        conn.commit()


put_into_sql(res_data)
conn.close()
