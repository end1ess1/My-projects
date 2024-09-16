import requests
from bs4 import BeautifulSoup
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Referer': 'https://www.kinoafisha.info/',
    'Origin': 'https://www.kinoafisha.info'}

url = 'https://www.kinoafisha.info/releases/archive/2023/'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')

data = soup.find_all('div', class_='archiveList_item inner-mobile')


def get_links():
    for one_data in data:
        data_links = one_data.find_all(
            'a', class_='archiveList_movie')
        for link in data_links:
            yield 'https://' + link.get('href').lstrip('/')


def to_list(x):
    return [i.text for i in x]


def array():
    for url_page in get_links():
        sleep(2)
        # код новой страницы
        response_page = requests.get(url_page, headers=headers)
        soup_page = BeautifulSoup(response_page.text, 'lxml')

        # атрибуты фильма
        title = soup_page.find('h1', class_='trailer_title').text[:-6]

        data_rating = soup_page.find(
            'div', class_='trailer_rating rating rating-detailed js-allowVote outer-mobile')
        if 'rating_num' in str(data_rating):
            rating = soup_page.find('span', class_='rating_num').text
        else:
            rating = 'NULL'
        if 'rating_votes' in str(data_rating):
            rating_votes = soup_page.find('span', class_='rating_votes').text
            rating_votes = ''.join([i for i in rating_votes if i.isdigit()])
        else:
            rating_votes = 'NULL'
        if 'rating_imdb' in str(data_rating):
            rating_imdb = soup_page.find(
                'span', class_='rating_imdb imdbRatingPlugin').text
            rating_imdb = ''.join(
                [i for i in rating_imdb if i.isdigit() or i == '.'])
        else:
            rating_imdb = 'NULL'
        genres = to_list(soup_page.find_all(
            'span', class_='filmInfo_genreItem button-main'))

        data_items = soup_page.find(
            'div', class_='filmInfo_info swipe outer-mobile inner-mobile')
        if 'filmInfo_infoData filmInfo_infoData-link' in str(data_items):
            movie_distributor = soup_page.find(
                'a', class_='filmInfo_infoData filmInfo_infoData-link').text
        else:
            movie_distributor = 'NULL'

        producer_and_actors = to_list(
            soup_page.find_all('span', class_='badgeList_name'))
        if len(producer_and_actors) < 2:
            producer_and_actors += (['NULL'] * (2 - len(producer_and_actors)))

        # Cловарь из дополнительных атрибутов
        data_info = {'Продолжительность': 'NULL',
                     'Год выпуска': 'NULL',
                     'Премьера в России': 'NULL',
                     'Премьера в мире': 'NULL',
                     'Премьера онлайн': 'NULL',
                     'Возраст': 'NULL',
                     'MPAA': 'NULL',
                     'Бюджет': 'NULL',
                     }
        category_names = to_list(soup_page.find_all(
            'span', class_='filmInfo_infoName'))
        if 'Прокатчик' in category_names:
            category_names.pop(category_names.index('Прокатчик'))
        category_values = to_list(soup_page.find_all(
            'span', class_='filmInfo_infoData'))
        slovar = dict(list(zip(category_names, category_values)))
        data_info = data_info | slovar

        # Возвращаем кортеж
        yield (title,
               rating,
               rating_votes,
               rating_imdb,
               genres,
               data_info,
               movie_distributor,
               producer_and_actors
               )
