import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from models import Auto
from environs import Env
from db_client import PostgresConnection
# from client_Max import DB_Postgres
from dataclasses import astuple

env = Env()
env.read_env()

DBNAME = env('DBNAME')
DBUSER = env('DBUSER')
DBPASSWORD = env('DBPASSWORD')
DBHOST = env('DBHOST')
DBPORT = env('DBPORT')


class AutoDB(PostgresConnection):

    def save_data(self, data: list[Auto]) -> None:
        data = [astuple(i) for i in data]
        self.update_query('''WITH auto_id as (
        INSERT INTO car_app_auto
        (id_car,
        link,
        price_usd,
        price_byn,
        price_eur,
        price_rub,
        city_location,
        seller,
        description,
        exchange,
        organization,
        year,
        brand,
        model,
        condition,
        alloy_wheels,
        abs,
        esp,
        anti_slip_system,
        immobilizer,
        front_safebags,
        side_safebags,
        rear_safebags,
        rain_detector,
        rear_view_camera,
        parktronics,
        hatch,
        cruise_control,
        steering_wheel_media_control,
        electro_seat_adjustment,
        front_glass_lift,
        rear_glass_lift,
        seat_heating,
        mirror_heating,
        steering_wheel_heating,
        climate_control,
        aux_ipod,
        bluetooth,
        cd_mp3_player,
        usb,
        media_screen,
        xenon_lights,
        fog_lights,
        led_lights,
        generation,
        number_of_seats,
        engine_capacity,
        engine_type,
        transmission_type,
        generation_with_years,
        interior_color,
        interior_material,
        body_type,
        drive_type,
        color,
        mileage_km)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
         %s, %s)
        
        RETURNING id
        )
        INSERT INTO car_app_image (image, auto_id) VALUES (unnest(COALESCE(%s, ARRAY[]::text[])), (SELECT id FROM auto_id))
        
        ''', data)

    def create_table(self):
        self.update_query('''
        CREATE TABLE IF NOT EXISTS auto_aw (
        id SERIAL PRIMARY KEY,
        id_car varchar(160) UNIQUE,
        link varchar(160) UNIQUE,
        price_usd INTEGER,
        price_byn INTEGER,
        price_eur INTEGER,
        price_rub INTEGER,
        city_location varchar(100),
        seller varchar(100),
        description TEXT,
        exchange varchar(100),
        organization varchar(100),
        year varchar(100),
        brand varchar(100),
        model varchar(100),
        condition varchar(100),
        alloy_wheels varchar(100),
        abs varchar(100),
        esp varchar(100),
        anti_slip_system varchar(100),
        immobilizer varchar(100),
        front_safebags varchar(100),
        side_safebags varchar(100),
        rear_safebags varchar(100),
        rain_detector varchar(100),
        rear_view_camera varchar(100),
        parktronics varchar(100),
        hatch varchar(100),
        cruise_control varchar(100),
        steering_wheel_media_control varchar(100),
        electro_seat_adjustment varchar(100),
        front_glass_lift varchar(100),
        rear_glass_lift varchar(100),
        seat_heating varchar(100),
        mirror_heating varchar(100),
        steering_wheel_heating varchar(100),
        climate_control varchar(100),
        aux_ipod varchar(100),
        bluetooth varchar(100),
        cd_mp3_player varchar(100),
        usb varchar(100),
        media_screen varchar(100),
        xenon_lights varchar(100),
        fog_lights varchar(100),
        led_lights varchar(100),
        generation varchar(100),
        number_of_seats varchar(100),
        engine_capacity varchar(100),
        engine_type varchar(100),
        transmission_type varchar(100),
        generation_with_years varchar(100),
        interior_color varchar(100),
        interior_material varchar(100),
        body_type varchar(100),
        drive_type varchar(100),
        color varchar(100),
        mileage_km INTEGER
        );
        CREATE TABLE IF NOT EXISTS image_auto(
        id serial PRIMARY KEY,
        image varchar(160) UNIQUE,
        auto_id integer REFERENCES auto_aw(id)
        )
        ''')


class ParserAuto:
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
               'Connection': 'keep-alive'
               }
    # PROXIES = {'http': 'http://50.172.75.127:80'}
    DB = AutoDB(
        DBNAME, DBUSER, DBPASSWORD, DBHOST, DBPORT
    )

    @classmethod
    def get_soup(cls, url: str) -> BeautifulSoup:
        response = requests.get(url, headers=cls.HEADERS)
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
        response = requests.get(f'https://api.av.by/offers/{id_car}', headers=cls.HEADERS).text
        data = json.loads(response)
        try:
            auto_data.link = data['publicUrl']
        except Exception as e:
            auto_data.link = ''
        try:
            auto_data.price_usd = data['price']['usd']['amount']
        except Exception as e:
            auto_data.price_usd = None
        try:
            auto_data.price_byn = data['price']['byn']['amount']
        except Exception as e:
            auto_data.price_byn = None
        try:
            auto_data.price_eur = data['price']['eur']['amount']
        except Exception as e:
            auto_data.price_eur = None
        try:
            auto_data.price_rub = data['price']['rub']['amount']
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
        properties = data['properties']
        for i in properties:
            if i['id'] == 4:
                auto_data.generation = i['value']
            elif i['id'] == 8:
                auto_data.number_of_seats = i['value']
            elif i['id'] == 13:
                auto_data.engine_capacity = i['value']
            elif i['id'] == 14:
                auto_data.engine_type = i['value']
            elif i['id'] == 7:
                auto_data.transmission_type = i['value']
            elif i['id'] == 5:
                auto_data.generation_with_years = i['value']
            elif i['id'] == 53:
                auto_data.alloy_wheels = i['value']
            elif i['id'] == 23:
                auto_data.abs = i['value']
            elif i['id'] == 24:
                auto_data.esp = i['value']
            elif i['id'] == 25:
                auto_data.anti_slip_system = i['value']
            elif i['id'] == 26:
                auto_data.immobilizer = i['value']
            elif i['id'] == 28:
                auto_data.front_safebags = i['value']
            elif i['id'] == 29:
                auto_data.side_safebags = i['value']
            elif i['id'] == 30:
                auto_data.rear_safebags = i['value']
            elif i['id'] == 31:
                auto_data.rain_detector = i['value']
            elif i['id'] == 32:
                auto_data.rear_view_camera = i['value']
            elif i['id'] == 33:
                auto_data.parktronics = i['value']
            elif i['id'] == 20:
                auto_data.interior_color = i['value']
            elif i['id'] == 21:
                auto_data.interior_material = i['value']
            elif i['id'] == 35:
                auto_data.hatch = i['value']
            elif i['id'] == 48:
                auto_data.cruise_control = i['value']
            elif i['id'] == 49:
                auto_data.steering_wheel_media_control = i['value']
            elif i['id'] == 50:
                auto_data.electro_seat_adjustment = i['value']
            elif i['id'] == 51:
                auto_data.front_glass_lift = i['value']
            elif i['id'] == 52:
                auto_data.rear_glass_lift = i['value']
            elif i['id'] == 37:
                auto_data.seat_heating = i['value']
            elif i['id'] == 39:
                auto_data.mirror_heating = i['value']
            elif i['id'] == 40:
                auto_data.steering_wheel_heating = i['value']
            elif i['id'] == 42:
                auto_data.climate_control = i['value']
            elif i['id'] == 56:
                auto_data.aux_ipod = i['value']
            elif i['id'] == 57:
                auto_data.bluetooth = i['value']
            elif i['id'] == 58:
                auto_data.cd_mp3_player = i['value']
            elif i['id'] == 59:
                auto_data.usb = i['value']
            elif i['id'] == 60:
                auto_data.media_screen = i['value']
            elif i['id'] == 44:
                auto_data.xenon_lights = i['value']
            elif i['id'] == 45:
                auto_data.fog_lights = i['value']
            elif i['id'] == 46:
                auto_data.led_lights = i['value']
            elif i['id'] == 16:
                auto_data.body_type = i['value']
            elif i['id'] == 17:
                auto_data.drive_type = i['value']
            elif i['id'] == 18:
                auto_data.color = i['value']
            elif i['id'] == 12:
                auto_data.mileage_km = i['value']

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
        # self.DB.create_table()
        url = 'https://cars.av.by'
        url_brands = self.get_url_brands(self.get_soup(url))
        for url_brand in url_brands:
            flag = True
            list_token = []
            while flag:
                soup = self.get_soup(url_brand)
                if soup:
                    id_and_token = self.get_link_pagination_brand(soup)
                    id_cars = id_and_token[0]
                    cars = []
                    for id_car in id_cars:
                        auto_data = self.get_auto_data(id_car)
                        cars.append(auto_data)
                else:
                    continue
                pprint(cars)
                self.DB.save_data(cars)
                token = id_and_token[1]
                list_token.append(token)
                if len(list_token) > len(set(list_token)) or not token:
                    flag = False
                url_brand = 'https://cars.av.by'+token
            list_token.pop()






parser = ParserAuto()
parser.run()


