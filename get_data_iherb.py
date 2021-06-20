import sqlite3
import requests
from bs4 import BeautifulSoup

DATABASE = '/var/www/u0733193/data/www/venisoking.ru/mapwars/warApp/iherb.db'
minerals = ['vitamin_a', 'vitamin_k', 'vitamin_e', 'vitamin_d', 'vitamin_c', 'vitamin_b', 'magnesium', 'zinc',
            'calcium', 'iron',
            'selenium', 'iodine', 'potassium', 'chromium', 'multimineral', 'trace',
            'boron', 'vanadyl', 'slilica_ortho_silicic_acid', 'lithium', 'manganese', 'copper',
            'molybdenum', 'silver', 'strontium', 'choline']

articles = ['vitamin']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}


def parse(query, page=1):
    site = 'https://ru.iherb.com/blog/search?kw={}&p={}'.format(query, page)
    html = requests.get(site, headers=headers)
    bsObj = BeautifulSoup(html.content, "html.parser")
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


def get_vitamin(query, limit=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    sql = "select * from vitamins"
    if 'type' in query:
        if query['type'] in minerals:
            sql += " where type='" + query['type'] + "'"
    if limit:
        sql += " limit " + str(limit)
    cursor.execute(sql)
    sqlResult = cursor.fetchall()
    conn.close()
    return sqlResult


def get_questions_func():
    d = {"data": [
        {"index": "0", "header": ["vitamin_a"],
         "questions": {"Ломкость волос": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "Сухость кожи": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "Ухудшение зрения": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "Появление полос на ногтях": ["Не указано", "Нет", "Да"]}},
        {"index": "1", "header": ["vitamin_b"],
         "questions": {"боли в животе": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "тошнота": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "повышенная утомляемость": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "деформации костей": ["Не указано", "0", "1", "2", "3"],
                       "снижение защитных сил организма": ["Не указано", "0", "1", "2", "3", "4", "5"]
                       }},
        {"index": "2", "header": ["vitamin_e", "vitamin_k"],
         "questions": {"неврологические расстройства": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "обильные кровотечения": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "гематомы на коже": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "нарушение прочности сосудов": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "повышенная кровоточивость десен": ["Не указано", "0", "1", "2", "3", "4", "5"]}},
        {"index": "3", "header": ["vitamin_c"],
         "questions": {
             "склонность к кровоизлиянию": ["Не указано", "0", "1", "2", "3", "4", "5"],
             "сухость кожи": ["Не указано", "0", "1", "2", "3", "4", "5"],
             "апатия": ["Не указано", "0", "1", "2", "3", "4", "5"],
             "учащение сердцебиения": ["Не указано", "0", "1", "2", "3", "4", "5"]}},
        {"index": "4", "header": ["vitamin_b", "vitamin_b1"],
         "questions": {"кожная сыпь": ["Не указано", "Нет", "Слабая", "Сильная"],
                       "дерматит": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "покраснение кожи": ["Не указано", "Нет", "Умеренное", "Сильное"],
                       "ощущение покалывания в руках": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "мышечные судороги и боли": ["Не указано", "Нет", "Редко", "Часто"],
                       "атрофия или паралич мышц": ["Не указано", "Нет", "Да"]}},
        {"index": "5", "header": ["vitamin_b2", "vitamin_b6"],
         "questions": {"потеря веса": ["Не указано", "Отсутствует", "Умеренная", "Сильная"],
                       "анемия": ["Не указано", "Нет", "Да"],
                       "нарушение заживления ран": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       "слабость": ["Не указано", "Нет", "Умеренная", "Сильная"],
                       "расстройства пищеварения": ["Не указано", "0", "1", "2", "3", "4", "5"],
                       }
         },
        {"index": "6", "header": ["vitamin_b6", "vitamin_b2"],
         "questions": {
             "высыпания на коже": ["Не указано", "Нет", "Слабые", "Сильные"],
             "трещинки в уголках рта": ["Не указано", "Нет", "Да"],
             "бессонница": ["Не указано", "Нет", "Небольшая", "Сильная"],
             "снижение аппетита": ["Не указано", "0", "1", "2", "3", "4", "5"],
             "ослабление иммунитета": ["Не указано", "0", "1", "2", "3", "4", "5"],
             "бесконтрольные движения": ["Не указано", "Нет", "Да"]}},
    ]}
    return d


def get_article_func(query):
    sql = "SELECT name, href, img, date, text, query from articles"
    result = []
    if 'keyword' in query:
        if query['keyword'] in articles:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            sql += " where query='" + query['keyword'] + "'"
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.close()
    if 'query' in query:
        if 'page' in query:
            result = parse(query['query'], page=query['page'])
        else:
            result = parse(query['query'])
    return result


def count_percents(answers):
    data = {'Недостаток A': 0.11, 'Переизбыток A': 0.11, 'Недостаток B': 0.1,
            'Недостаток C': 0.12, 'Недостаток D': 0.12, 'Переизбыток D': 0.1,
            'Недостаток B1': 0.05, 'Переизбыток B6': 0.06, 'Недостаток B6': 0.04,
            'Недостаток B2': 0.07, 'Недостаток E': 0.1}
    prepared_answers = answers
    if isinstance(prepared_answers, str):
        prepared_answers = eval(prepared_answers)
    if 'questions' not in prepared_answers:
        for i in answers.items():
            prepared_answers = eval(i[0])
            break
    try:
        height, weight, city, sex, birthData = prepared_answers["height"], prepared_answers["weight"], prepared_answers[
            "city"], \
                                               prepared_answers["sex"], prepared_answers["birth_date"]
    except:
        height, weight, city, sex, birthData = 0, 0, '', '', ''
    weight = int(weight)
    height = int(height)
    if weight > 100:
        for elem in data:
            data[elem] += 0.1
    if isinstance(prepared_answers, str):
        prepared_answers = eval(prepared_answers)
    question_req = prepared_answers['questions']

    if isinstance(question_req, str):
        question_req = eval(question_req)

    for question in question_req:
        with open('log.txt', 'at') as f:
            f.write(question)
            f.write('\t')
            f.write(question_req[question])
            f.write('\n')
        if question == "Ломкость волос":
            if question_req[question] == "1":
                data['Недостаток A'] += 0
                data['Недостаток C'] += 0.03
            elif question_req[question] == "2":
                data['Недостаток A'] += 0.06
                data['Недостаток C'] += 0.06
            elif question_req[question] == "3":
                data['Недостаток A'] += 0.1
                data['Недостаток C'] += 0.1
            elif question_req[question] == "4":
                data['Недостаток A'] += 0.125
                data['Недостаток C'] += 0.125
            elif question_req[question] == "5":
                data['Недостаток A'] += 0.18
                data['Недостаток C'] += 0.18
        elif question == "Сухость кожи":
            if question_req[question] == "1":
                data['Недостаток C'] += 0
            elif question_req[question] == "2":
                data['Недостаток C'] += 0.06
            elif question_req[question] == "3":
                data['Недостаток C'] += 0.1
            elif question_req[question] == "4":
                data['Недостаток C'] += 0.12
            elif question_req[question] == "5":
                data['Недостаток C'] += 0.16
        elif question == "Ухудшение зрения":
            if question_req[question] == "1":
                data['Недостаток A'] += 0
            elif question_req[question] == "2":
                data['Недостаток A'] += 0.06
            elif question_req[question] == "3":
                data['Недостаток A'] += 0.1
            elif question_req[question] == "4":
                data['Недостаток A'] += 0.125
            elif question_req[question] == "5":
                data['Недостаток A'] += 0.18
        elif question == "Появление полос на ногтях":
            pass
        elif question == "боли в животе":
            if question_req[question] == "1":
                data['Переизбыток A'] += 0
            elif question_req[question] == "2":
                data['Переизбыток A'] += 0.05
                data['Недостаток A'] -= 0.01
            elif question_req[question] == "3":
                data['Переизбыток A'] += 0.07
                data['Недостаток A'] -= 0.03
            elif question_req[question] == "4":
                data['Переизбыток A'] += 0.1
                data['Недостаток A'] -= 0.05
            elif question_req[question] == "5":
                data['Переизбыток A'] += 0.12
                data['Недостаток A'] -= 0.05
        elif question == "тошнота":
            if question_req[question] == "1":
                data['Переизбыток A'] += 0
                data['Недостаток A'] -= 0
            elif question_req[question] == "2":
                data['Переизбыток A'] += 0.05
                data['Недостаток A'] -= 0.02
            elif question_req[question] == "3":
                data['Переизбыток A'] += 0.07
                data['Недостаток A'] -= 0.03
            elif question_req[question] == "4":
                data['Переизбыток A'] += 0.1
                data['Недостаток A'] -= 0.04
            elif question_req[question] == "5":
                data['Переизбыток A'] += 0.12
                data['Недостаток A'] -= 0.05
        elif question == "повышенная утомляемость":
            if question_req[question] == "1":
                data['Переизбыток A'] += 0
                data['Недостаток D'] += 0.03
            elif question_req[question] == "2":
                data['Переизбыток A'] += 0.05
                data['Недостаток D'] += 0.05
            elif question_req[question] == "3":
                data['Переизбыток A'] += 0.07
                data['Недостаток D'] += 0.07
            elif question_req[question] == "4":
                data['Переизбыток A'] += 0.1
                data['Недостаток D'] += 0.09
            elif question_req[question] == "5":
                data['Переизбыток A'] += 0.12
                data['Недостаток D'] += 0.13
        elif question == "деформации и нарушение роста костей":
            if question_req[question] == "1":
                data['Недостаток D'] += 0
            elif question_req[question] == "2":
                data['Недостаток D'] += 0.05
            elif question_req[question] == "3":
                data['Недостаток D'] += 0.07
        elif question == "снижение защитных сил организма":
            if question_req[question] == "1":
                data['Недостаток D'] += 0
            elif question_req[question] == "2":
                data['Недостаток D'] += 0.05
            elif question_req[question] == "3":
                data['Недостаток D'] += 0.07
            elif question_req[question] == "4":
                data['Недостаток D'] += 0.09
            elif question_req[question] == "5":
                data['Недостаток D'] += 0.13
        elif question == "неврологические расстройства":
            if question_req[question] == "1":
                data['Недостаток E'] += 0
            elif question_req[question] == "2":
                data['Недостаток E'] += 0.06
            elif question_req[question] == "3":
                data['Недостаток E'] += 0.08
            elif question_req[question] == "4":
                data['Недостаток E'] += 0.10
            elif question_req[question] == "5":
                data['Недостаток E'] += 0.14
        elif question == "обильные кровотечения":
            if question_req[question] == "1":
                data['Недостаток C'] += 0
            elif question_req[question] == "2":
                data['Недостаток C'] += 0.06
            elif question_req[question] == "3":
                data['Недостаток C'] += 0.08
            elif question_req[question] == "4":
                data['Недостаток C'] += 0.10
            elif question_req[question] == "5":
                data['Недостаток C'] += 0.14
        elif question == "гематомы на коже":
            # data['Недостаток K'] += 0.18
            pass
        elif question == "нарушение прочности сосудов":
            pass
        elif question == "повышенная кровоточивость десен":
            if question_req[question] == "1":
                data['Недостаток C'] += 0
            elif question_req[question] == "2":
                data['Недостаток C'] += 0.06
            elif question_req[question] == "3":
                data['Недостаток C'] += 0.08
            elif question_req[question] == "4":
                data['Недостаток C'] += 0.10
            elif question_req[question] == "5":
                data['Недостаток C'] += 0.14
        elif question == "склонность к кровоизлиянию":
            if question_req[question] == "1":
                data['Недостаток C'] += 0
            elif question_req[question] == "2":
                data['Недостаток C'] += 0.06
            elif question_req[question] == "3":
                data['Недостаток C'] += 0.08
            elif question_req[question] == "4":
                data['Недостаток C'] += 0.10
            elif question_req[question] == "5":
                data['Недостаток C'] += 0.14
        elif question == "сухость кожи":
            if question_req[question] == "1":
                data['Недостаток C'] += 0
                data['Недостаток A'] += 0
                data['Недостаток B6'] += 0
            elif question_req[question] == "2":
                data['Недостаток C'] += 0.03
                data['Недостаток A'] += 0.03
                data['Недостаток B6'] += 0.03
            elif question_req[question] == "3":
                data['Недостаток C'] += 0.06
                data['Недостаток A'] += 0.06
                data['Недостаток B6'] += 0.06
            elif question_req[question] == "4":
                data['Недостаток C'] += 0.08
                data['Недостаток A'] += 0.08
                data['Недостаток B6'] += 0.08
            elif question_req[question] == "5":
                data['Недостаток C'] += 0.1
                data['Недостаток A'] += 0.1
                data['Недостаток B6'] += 0.1
        elif question == "апатия":
            if question_req[question] == "1":
                data['Недостаток C'] += 0
            elif question_req[question] == "2":
                data['Недостаток C'] += 0.06
            elif question_req[question] == "3":
                data['Недостаток C'] += 0.08
            elif question_req[question] == "4":
                data['Недостаток C'] += 0.10
            elif question_req[question] == "5":
                data['Недостаток C'] += 0.12
        elif question == "учащение сердцебиения":
            if question_req[question] == "1":
                data['Недостаток C'] += 0
            elif question_req[question] == "2":
                data['Недостаток C'] += 0.03
            elif question_req[question] == "3":
                data['Недостаток C'] += 0.06
            elif question_req[question] == "4":
                data['Недостаток C'] += 0.08
            elif question_req[question] == "5":
                data['Недостаток C'] += 0.11
        elif question == "кожная сыпь":
            if question_req[question] == "Нет":
                data['Недостаток B6'] += 0
                data['Недостаток B1'] += 0
                data['Недостаток B2'] += 0
            elif question_req[question] == "Слабая":
                data['Недостаток B6'] += 0.04
                data['Недостаток B1'] += 0.04
                data['Недостаток B2'] += 0.04
            elif question_req[question] == "Сильная":
                data['Недостаток B6'] += 0.08
                data['Недостаток B1'] += 0.08
                data['Недостаток B2'] += 0.08
        elif question == "дерматит":
            if question_req[question] == "1":
                data['Недостаток B6'] += 0
                data['Недостаток B1'] += 0
                data['Недостаток B2'] += 0
            elif question_req[question] == "2":
                data['Недостаток B6'] += 0.03
                data['Недостаток B1'] += 0.03
                data['Недостаток B2'] += 0.03
            elif question_req[question] == "3":
                data['Недостаток B6'] += 0.06
                data['Недостаток B1'] += 0.06
                data['Недостаток B2'] += 0.06
            elif question_req[question] == "4":
                data['Недостаток B6'] += 0.08
                data['Недостаток B1'] += 0.08
                data['Недостаток B2'] += 0.08
            elif question_req[question] == "5":
                data['Недостаток B6'] += 0.1
                data['Недостаток B1'] += 0.1
                data['Недостаток B2'] += 0.1
        elif question == "покраснение кожи":
            if question_req[question] == "Нет":
                data['Недостаток B6'] += 0
                data['Недостаток B1'] += 0
                data['Недостаток B2'] += 0
            elif question_req[question] == "Умеренное":
                data['Недостаток B6'] += 0.03
                data['Недостаток B1'] += 0.03
                data['Недостаток B2'] += 0.03
            elif question_req[question] == "Сильное":
                data['Недостаток B6'] += 0.06
                data['Недостаток B1'] += 0.06
                data['Недостаток B2'] += 0.06
            elif question_req[question] == "4":
                data['Недостаток B6'] += 0.08
                data['Недостаток B1'] += 0.08
                data['Недостаток B2'] += 0.08
            elif question_req[question] == "5":
                data['Недостаток B6'] += 0.1
                data['Недостаток B1'] += 0.1
                data['Недостаток B2'] += 0.1
        elif question == "ощущение покалывания в руках и ногах":
            if question_req[question] == "1":
                data['Недостаток B6'] += 0
                data['Недостаток B1'] += 0
                data['Недостаток B2'] += 0
            elif question_req[question] == "2":
                data['Недостаток B6'] += 0.03
                data['Недостаток B1'] += 0.03
                data['Недостаток B2'] += 0.03
            elif question_req[question] == "3":
                data['Недостаток B6'] += 0.06
                data['Недостаток B1'] += 0.06
                data['Недостаток B2'] += 0.06
            elif question_req[question] == "4":
                data['Недостаток B6'] += 0.08
                data['Недостаток B1'] += 0.08
                data['Недостаток B2'] += 0.08
            elif question_req[question] == "5":
                data['Недостаток B6'] += 0.1
                data['Недостаток B1'] += 0.1
                data['Недостаток B2'] += 0.1
        elif question == "мышечные судороги и боли":
                data['Недостаток B6'] += 0.03
                data['Недостаток B1'] += 0.03
                data['Недостаток B2'] += 0.03
        elif question == "атрофия или паралич мышц":
                data['Недостаток D'] += 0.03
        elif question == "потеря веса":
                data['Недостаток A'] += 0.03
                data['Недостаток C'] += 0.03
                data['Недостаток D'] += 0.03
        elif question == "анемия":
                data['Недостаток B6'] += 0.03
                data['Недостаток B1'] += 0.03
                data['Недостаток B2'] += 0.03
        elif question == "нарушение заживления ран":
                data['Недостаток C'] += 0.03
                data['Недостаток A'] += 0.03
        elif question == "слабость":
                data['Недостаток C'] += 0.03
        elif question == "расстройства пищеварения":
                data['Недостаток A'] += 0.03
                data['Недостаток C'] += 0.03
        elif question == "высыпания на коже":
                data['Недостаток E'] += 0.03
                data['Недостаток A'] += 0.03
                data['Недостаток B2'] += 0.03
        elif question == "трещинки в уголках рта":
            if question_req[question] == "Да":
                data['Недостаток B6'] += 0.1
                data['Недостаток B1'] += 0.1
                data['Недостаток B2'] += 0.1
        elif question == "бессонница":
            pass
        elif question == "снижение аппетита":
            if question_req[question] == "1":
                data['Недостаток A'] += 0
            elif question_req[question] == "2":
                data['Недостаток A'] += 0.03
            elif question_req[question] == "3":
                data['Недостаток A'] += 0.06
            elif question_req[question] == "4":
                data['Недостаток A'] += 0.08
            elif question_req[question] == "5":
                data['Недостаток A'] += 0.11
        elif question == "ослабление иммунитета":
            if question_req[question] == "1":
                data['Недостаток B'] += 0
                data['Недостаток C'] += 0
            elif question_req[question] == "2":
                data['Недостаток B'] += 0.03
                data['Недостаток C'] += 0.03
            elif question_req[question] == "3":
                data['Недостаток B'] += 0.06
                data['Недостаток C'] += 0.06
            elif question_req[question] == "4":
                data['Недостаток B'] += 0.09
                data['Недостаток C'] += 0.09
            elif question_req[question] == "5":
                data['Недостаток B'] += 0.11
                data['Недостаток C'] += 0.11
        elif question == "потеря контроля над движениями":
            pass
    # data = {'Недостаток A': 0.44, 'Переизбыток A': 0.17, 'Недостаток B': 0.12,
    #              'Недостаток C': 0.61, 'Недостаток D': 0.36, 'Переизбыток D': 0.13,
    #              'Недостаток B1': 0.71, 'Переизбыток B6': 0.18, 'Недостаток B6': 0.14,
    #              'Недостаток B2': 0.25, 'Недостаток E': 0.1}
    max_elem = -1
    max_value = 0
    for elem in data:
        if data[elem] > 0.8:
            data[elem] = 0.79
        if max_value < data[elem] and 'Недостаток' in elem:
            max_elem = elem
            max_value = data[elem]
    if max_value < 0.5:
        data[max_elem] *= 1.3
    for elem in data:
        data[elem] = round(data[elem], 2)
    return data, (max_elem, max_value)


def decision(request):
    d = {'Недостаток A': ['vitamin_a', ['Витамин E', 'Витамин C', 'Цинк', 'Железо'], ['Витамин B12', 'Витамин K']],
         'Недостаток B': ['vitamin_b'],
         'Недостаток C': ['vitamin_c', ['Витамин A', 'Витамин B5', 'Витамин B9', 'Витамин E', 'Железо', 'Кальций'],
                          ['Витамин B1', 'Витамин B12', 'Медь']],
         'Недостаток D': ['vitamin_d', ['Кальций', 'Фосфор'], ['Витамин E']],
         'Недостаток B1': ['vitamin_b', ['Витамин B5'], ['Витамин B2', 'Витамин B6', 'Витамин B3', 'Витамин B12',
                                                         'Витамин C']],
         'Недостаток B6': ['vitamin_b'],
         'Недостаток B2': ['vitamin_b', ['Витамин B3', 'Витамин B5', 'Витамин B6', 'Витамин B9',
                                         'Витамин K', 'Цинк'], ['Витамин B1', 'Витамин B12', 'Железо', 'Медь']],
         'Недостаток E': ['vitamin_e', ['Витамин A', 'Витамин C'],
                          ['Витамин D', 'Витамин B12', 'Витамин K', 'Железо', 'Магний', 'Медь']]}
    querries_article = {'Недостаток A': 'витамин A', 'Недостаток B': 'витамин B',
                        'Недостаток C': 'витамин C', 'Недостаток D': 'витамин D',
                        'Недостаток B1': 'витамин B1', 'Недостаток B6': 'витамин B6',
                        'Недостаток B2': 'витамин B2', 'Недостаток E': ['витамин E']}
    data, max_elem = count_percents(request)
    # data = {'Недостаток A': 0.44, 'Переизбыток A': 0.17, 'Недостаток B': 0.12,
    #         'Недостаток C': 0.61, 'Недостаток D': 0.36, 'Переизбыток D': 0.13,
    #         'Недостаток B1': 0.71, 'Переизбыток B6': 0.18, 'Недостаток B6': 0.14,
    #         'Недостаток B2': 0.25, 'Недостаток E': 0.1}
    res = {'показания': [], 'to_add': set(), 'not_to_add': set()}
    # {'order': '', 'medicine': [], 'articles': [], 'to_add': [], 'not_to_add': []}
    for elem in data:
        if elem == max_elem or data[elem] > 0.5:
            if elem in d:
                todo = {'medicine': [], 'articles': []}
                for i in get_vitamin({'type': d[elem][0]}, 4):
                    todo['medicine'].append(list(i))
                # todo['medicine'] +=
                todo['articles'] += parse(querries_article[elem])
                todo['order'] = elem
                # todo['to_add'] = d[elem][1]
                # todo['not_to_add'] = d[elem][2]
                res['показания'].append(todo)
                for i in d[elem][1]:
                    res['to_add'].add(i)
                for i in d[elem][2]:
                    res['not_to_add'].add(i)
    for elem in res['not_to_add']:
        if elem in res['to_add']:
            res['to_add'].remove(elem)
    res['diagnosis'] = data
    res['to_add'] = list(res['to_add'])
    res['not_to_add'] = list(res['not_to_add'])
    return res
