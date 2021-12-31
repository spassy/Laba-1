import csv
import json
import sqlite3

import requests
from bs4 import BeautifulSoup
from lxml import etree
from pip._internal.utils import encoding
import re


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
    }
    with open('projects.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    articles = soup.find_all('article',
                             class_='card card--catalog card--profession')  # Добавляем все ячейки с профессиями

    project_urls = []
    args = []
    timet = []
    for article in articles:  # Перебираем эти ячейки, для добавление ссылок на каждую из наш профессия
        project_url = article.find('a').get('href')
        project_time = article.find('b', class_='card__count').text
        project_time_out = re.sub(r'\n ', '', str(project_time))
        project_time_outt = re.sub(r'\s+', '', str(project_time_out))
        timet.append((project_time_outt))
        project_urls.append(project_url)
    print(timet)

    for project_url in project_urls:
        req = requests.get(project_url, headers)
        project_name = project_url.split('/')[-2]  # Забираем все ссылки на наши профессии

        with open(f"data/{project_name}.html", 'w') as file:
            print (project_name)
            file.write(req.text)

        with open(f"data/{project_name}.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        project_data = soup.find('body')
        name_curs = project_data.find('h1', class_='start-screen__title h h--1').text
        description_curs = project_data.find('p', class_='start-screen__desc').text
        cost_curs = project_data.find('li', class_='price-info__item').text
        cost_curs_out = re.sub(r'₽ /мес', '', str(cost_curs))
        name_curs_out = re.sub(r'Профессия', '', str(name_curs))
        args.append((name_curs_out, description_curs, cost_curs_out))
    print(args)
    conn = sqlite3.connect('skill.db')

    cursor = conn.cursor()

    cursor.executemany('INSERT INTO skillbox (Profession,Description,Price) VALUES (?,?,?)', args)
    # cursor.executemany('INSERT INTO skillbox (Time) VALUES (?)', timet)
    conn.commit()
    conn.close()


get_data('https://skillbox.ru/code/')
