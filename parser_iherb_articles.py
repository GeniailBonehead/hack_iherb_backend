import requests
from bs4 import BeautifulSoup
import sqlite3

base_site = 'https://ru.iherb.com/blog/all?p='
base_site = 'https://ru.iherb.com/blog/search?kw=витамин&p='

conn = sqlite3.connect('/home/vitt/Документы/iherb.db')
cursor = conn.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}

def parse(site, query):
    html = requests.get(site, headers=headers)
    bsObj = BeautifulSoup(html.content, "lxml")
    articles = bsObj.find_all('article', class_='article-preview')
    data = []
    for article in articles:
        line = dict()
        name = article.contents[1].get('aria-label')
        name = name.replace(' Link', '')
        href = article.contents[1].get('href')
        href = 'https://ru.iherb.com' + href
        img = article.contents[3].find('img').get('src')
        date = article.contents[5].find('div', class_='small iherb-article-date').text
        date = date.replace('\n', '').replace('            ', '').replace('        ', '')
        text = article.contents[5].find('div', class_='text-container hidden-xs hidden-sm').text
        text = text.replace('\n', '').replace('            ', '').replace('        ', '')
        line['name'] = name
        line['href'] = href
        line['img'] = img
        line['date'] = date
        line['text'] = text
        line['query'] = query
        data.append(line)
    return data

res_data = []
for i in range(1, 27):
    print(i)
    site = base_site + str(i)
    res_data += parse(site, 'all')

# res_data = parse(base_site+'1', 'vitamin_d')


def put_into_sql(data):
    for line in data:
        sql = """INSERT INTO articles (name, href, img, date, text, query) VALUES ("""
        sql += "'" + line['name'] + "', '" + line['href'] + "', '" + line['img'] + \
               "', '" + line['date'] + "', '" + line['text'] + "', '" + line['query'] +"')"
        # print(sql)
        cursor.execute(sql)
        conn.commit()


def update_sql(data):
    for line in data:
        sql = "UPDATE articles set query='vitamin' where href='" + line['href'] + "'"
        cursor.execute(sql)
        conn.commit()


# put_into_sql(res_data)
update_sql(res_data)
conn.close()
