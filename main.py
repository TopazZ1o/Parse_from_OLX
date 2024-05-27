import os
import requests
import xlsxwriter
import locale
from bs4 import BeautifulSoup
from datetime import datetime
from Levenshtein import ratio

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

# os.makedirs("infoOLX", exist_ok=True)

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
        # print(similarity_score)
        if similarity_score >= 0.6:
            publication_date = curr_date.strftime('%d %B %Y г.')

        print(publication_date)
        # if publication_date.lower() in ['Сегодня']:
        #     new_date = curr_date.strftime('%d, %B, Y')
        #     data.append([name_block, new_date, output_post_link])
        #     print(new_date)
        # else:
        #     data.append([name_block, publication_date, output_post_link])
        data.append([name_block, publication_date, output_post_link])
        # data.append([name_block, output_post_link])

with xlsxwriter.Workbook('Posts.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    for row_num, info in enumerate(data):
        worksheet.write_row(row_num, 0, info)

    # necessary_bs = BeautifulSoup(storage, 'lxml')
    # necessary_block = necessary_bs.find('div', class_ = 'entry-content')
    # name_block = necessary_bs.find('h1', class_ = 'entry-title')
    # if name_block:
    #     name_block_text = name_block.text
    #     name_block_editied = (name_block_text.replace('/', '.').replace('?', '.').
    #                           replace(':', '.').replace('*', '.').replace('"', '.').
    #                           replace('<', '.').replace('>', '.').replace('|', '.').
    #                           replace('\"', '.'))
    #     result_link = None
    #     for link in necessary_block.find_all('a'):
    #         if ('open.acast.com' in link.get('href') or 'traffic.libsyn.com' in link.get('href')
    #                 or 'hotenov.com' in link.get('href')):
    #             result_link = link.get('href')
    #             break
    #     if result_link:
    #         necessary_audio = requests.get(result_link).content
    #
    #         with open(f'infoOLX/{name_block_editied}.mp3', 'wb') as file:
    #             file.write(necessary_audio)
    #
    #         print(f'аудио {name_block_editied}.mp3 скачалось')
    #     else:
    #         print("Ссылка на аудио не найдена")
    # else:
    #     print("Элемент не найден")

