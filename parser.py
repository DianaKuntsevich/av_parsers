import json

import requests
from bs4 import BeautifulSoup
from models import Auto
from environs import Env
from db_client import PostgresConnection
from dataclasses import astuple

env = Env()
env.read_env()

DBNAME = env('DBNAME')
DBUSER = env('DBUSER')
DBPASSWORD = env('DBPASSWORD')
DBHOST = env('DBHOST')
DBPORT = env('DBPORT')


class ParserAuto:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive'
    }
    PROXIES = {
        'http': 'http://50.172.75.127:80'
    }

    @classmethod
    def get_soup(cls, url: str) -> BeautifulSoup:
        response = requests.get(url, headers=cls.HEADERS, proxies=cls.PROXIES)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        else:
            print(f'{url} | {response.status_code}')

    @staticmethod
    def get_url_brands(soup: BeautifulSoup) -> list:
        data = soup.find('script', id="__NEXT_DATA__").text
        data = json.loads(data)
        data = data['props']['initialState']
        data = data['landing']['seo']['links']
        url_brands = []
        for i in data:
            link_brand = i['url']
            url_brands.append(link_brand)

        return url_brands

    @staticmethod
    def get_link_pagination_brand(soup: BeautifulSoup) -> list:
        links = soup.find_all('a', class_='listing-item__link', href=True)
        id_cars = []
        for link in links:
            id_car = link.get('href').split('/')[-1]
            id_cars.append(id_car)
        try:
            next_page_token = soup.find_all('a', class_='button button--default', href=True)[-1].get('href')
        except Exception as e:
            next_page_token = ''

        return [id_cars, next_page_token]

    @classmethod
    def get_auto_data(cls, id_car: str) -> Auto:
        auto_data = Auto(id_car)
        response = requests.get(f'https://api.av.by/offers/{id_car}', headers=cls.HEADERS, proxies=cls.PROXIES).text
        data = json.loads(response)
        try:
            auto_data.link = data['publicUrl']
        except Exception as e:
            auto_data.link = ''
        try:
            auto_data.price_usd = data['price']['usd']['amountFiat']
        except Exception as e:
            auto_data.price_usd = None
        try:
            auto_data.price_byn = data['price']['byn']['amountFiat']
        except Exception as e:
            auto_data.price_byn = None
        try:
            auto_data.price_eur = data['price']['eur']['amountFiat']
        except Exception as e:
            auto_data.price_eur = None
        try:
            auto_data.price_rub = data['price']['rub']['amountFiat']
        except Exception as e:
            auto_data.price_rub = None
        try:
            auto_data.city_location = data['locationName']
        except Exception as e:
            auto_data.city_location = ''
        try:
            auto_data.seller = data['sellerName']
        except Exception as e:
            auto_data.seller = ''
        try:
            auto_data.description = data['description']
        except Exception as e:
            auto_data.description = ''
        try:
            auto_data.exchange = data['exchange']['label']
        except Exception as e:
            auto_data.exchange = ''
        try:
            auto_data.image = []
            images = data['photos']
            for image in images:
                photo = image['big']['url']
                auto_data.image.append(photo)
        except Exception as e:
            auto_data.image = []
        try:
            auto_data.organization = data['organizationTitle']
        except Exception as e:
            auto_data.organization = ''
        try:
            auto_data.year = data['year']
        except Exception as e:
            auto_data.year = None
        try:
            auto_data.brand = data['metadata']['brandSlug']
        except Exception as e:
            auto_data.brand = ''
        try:
            auto_data.condition = data['metadata']['condition']['label']
        except Exception as e:
            auto_data.condition = ''
        try:
            auto_data.model = data['metadata']['modelSlug']
        except Exception as e:
            auto_data.model = ''
        try:
            auto_data.properties = data['properties']
        except Exception as e:
            auto_data.properties = '0'

        return auto_data





    # def run(self):
    #     url = 'https://cars.av.by'
    #     flag = True
    #     while flag:
    #         url_brands = self.get_url_brands(self.get_soup(url))
    #         for url_brand in url_brands:
    #             soup = self.get_soup(url_brand)
    #             if soup:
    #                 id_and_token = self.get_link_pagination_brand(soup)
    #                 id_cars = id_and_token[0]
    #                 cars = []
    #                 for id_car in id_cars:
    #                     auto_data = self.get_auto_data(id_car)
    #                     cars.append(auto_data)
    #                 print(cars)
    #             else:
    #                 continue
    #             token = id_and_token[1]
    #             if not token:
    #                 flag = False
    #             url = f'https://cars.av.by{token}'

    def run(self):
        url = 'https://cars.av.by'
        url_brands = self.get_url_brands(self.get_soup(url))
        for url_brand in url_brands:
            flag = True
            list_token = []
            while flag:
                soup = self.get_soup(url_brand)
                if soup:
                    id_and_token = self.get_link_pagination_brand(soup)
                    # id_cars = id_and_token[0]
                    # cars = []
                    # for id_car in id_cars:
                    #     auto_data = self.get_auto_data(id_car)
                    #     cars.append(auto_data)
                    # print(cars)
                else:
                    continue
                token = id_and_token[1]
                list_token.append(token)
                if len(list_token) > len(set(list_token)) or not token:
                    flag = False
                url_brand = 'https://cars.av.by'+token
                print(url_brand)
            list_token.pop()






parser = ParserAuto()
parser.run()
