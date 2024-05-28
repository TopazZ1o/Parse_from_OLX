import os
import requests
import xlsxwriter
import locale
from bs4 import BeautifulSoup
from datetime import datetime
from Levenshtein import ratio

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

os.makedirs("infoOLX", exist_ok=True)

url = "https://www.olx.kz/"
link = f"/hobbi-otdyh-i-sport/sport-otdyh/astana/?page=1&search%5Border%5D=created_at%3Adesc"
data = [['Наименование', 'Кол-во просмотров', 'дата публикации', 'ссылка']]

curr_link = None
for page in range(1, 2):
    curr_link = f'/hobbi-otdyh-i-sport/sport-otdyh/astana/?page={page}&search%5Border%5D=created_at%3Adesc'

    response = requests.get(f'{url}/{curr_link}')

    bs = BeautifulSoup(response.text, "lxml")

    block = bs.find('div', class_ = 'listing-grid-container css-d4ctjd')
    post_class = block.find_all('div', class_='css-u2ayx9')

    for post in post_class:
        post_link = post.find_next('a').get('href')
        name_block = post.find('h6', class_='css-16v5mdi er34gjf0').text
        output_post_link = url + post_link

        storage = requests.get(f'{url}/{post_link}').text
        necessary_bs = BeautifulSoup(storage, 'lxml')

        # views_block = necessary_bs.find('div', class_='css-ayk4fp')
        # print(views_block)
        # views = views_block.find('span', class_='css-42xwsi')
        # print(views)

        publication_date_block = necessary_bs.find('div', class_='css-1yzzyg0')
        publication_date = publication_date_block.find('span', class_='css-19yf5ek').text

        curr_date = datetime.now()

        similarity_score = ratio(publication_date, 'Сегодня')
        if similarity_score >= 0.6:
            publication_date = curr_date.strftime('%d/%m/%Y')
        elif similarity_score < 0.6:
            publication_date = (publication_date.replace('января', 'январь')
                                .replace('февраля', 'февраль')
                                .replace('марта', 'март')
                                .replace('апреля', 'апрель')
                                .replace('мая', 'май')
                                .replace('июня', 'июнь')
                                .replace('июля', 'июль')
                                .replace('августа', 'август')
                                .replace('сентября', 'сентябрь')
                                .replace('октября', 'октябрь')
                                .replace('ноября', 'ноябрь')
                                .replace('декабря', 'декабрь'))
            change_date = datetime.strptime(publication_date, '%d %B %Y г.')
            publication_date = change_date.strftime('%d/%m/%Y')
        else:
            print("Дата публикации не найдена")

        print(name_block, publication_date, output_post_link)
        data.append([name_block, publication_date, output_post_link])

with xlsxwriter.Workbook('infoOLX/Posts.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, info in enumerate(data):
        worksheet.write_row(row_num, 0, info)