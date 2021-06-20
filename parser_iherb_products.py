import requests
from bs4 import BeautifulSoup
import sqlite3

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

print(parse('https://ru.iherb.com/pr/Life-Extension-BioActive-Complete-B-Complex-60-Vegetarian-Capsules/67051'))
