import csv
import logging
import re
import requests
import time

from selenium import webdriver
from time import sleep
from PIL import Image

from bs4 import BeautifulSoup
from sqlalchemy import create_engine

from pytesseract import image_to_string, pytesseract
from webapp.config import SQLALCHEMY_DATABASE_URI


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('avitobot.log', 'w',
                                                  'utf-8')]
                    )


site = 'https://www.avito.ru'
full_links_list = []
filtered_links = []
results = []
url_full = []
params_full = []
users_info = []
user_auto = []

translate = {
    'Владельцев по ПТС': 'holders', 'Поколение': 'generation',
    'Состояние': 'condition', 'Руль': 'steering_wheel', 'Привод': 'wheeldrive',
    'Цвет': 'color', 'Объём двигателя': 'engine_capacity', 'Модель': 'model',
    'Пробег': 'mileage', 'Марка': 'brand', 'Год выпуска': 'year',
    'Тип кузова': 'body_type', 'Тип двигателя': 'type_engine',
    'Коробка передач': 'gear', 'Мощность двигателя': 'power',
    'Количество дверей': 'doors', 'VIN или номер кузова': 'vin',
    'Место осмотра': 'location', 'Комплектация': 'equipment',
    'Модификация': 'modification'
 }


table_fields = [
          'id', 'name', 'price',
          'description', 'user_id',
          'active'
               ]
user_fields = [
    'id', 'name', 'street_address', 'number', 'role'
]

img_fields = [
    'auto_id', 'url_picture'
             ]

param_fields = [
    'auto_id', 'holders', 'generation', 'condition', 'steering_wheel',
    'wheeldrive',
    'color', 'engine_capacity', 'model', 'mileage', 'brand', 'year',
    'body_type', 'type_engine', 'gear', 'power', 'doors', 'vin',
    'location', 'equipment', 'modification'
                ]

csv_names = [
    'auto.csv', 'auto_img.csv', 'auto_params.csv', 'users.csv']

fields = [
    table_fields, img_fields, param_fields, user_fields]

material = [results, url_full, params_full, users_info]


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        logging.error('Ошибка сети.')
        return False


def get_links_from_pages():
    logging.info('Программа запущена.')
    page_num = 1
    while page_num <= 1:
        html = get_html(f'{site}/moskva/avtomobili?p={page_num}&radius=0')
        if html:
            logging.info(f'Работаем со страницей {page_num}')
            time.sleep(1.1)
            soup = BeautifulSoup(html, 'html.parser').find_all
            links_from_page = soup('a', class_="item-description-title-link")
            for link in links_from_page:
                full_links_list.append(link['href'])
        page_num += 1
    for link in list(set(full_links_list)):
        filtered_links.append(link)
    logging.info(f'Получены ссылки: {len(filtered_links)}.')
    return filtered_links


def get_link_info():
    try:
        for link in filtered_links:
            print(link)
            html = get_html(f"{site}{link}")
            logging.info('Делаю запрос по ссылке.')
            time.sleep(1.5)
            logging.info('Делаю паузу...')
            if html:
                soup = BeautifulSoup(html, 'html.parser').find
                soupAll = BeautifulSoup(html, 'html.parser').findAll
                try:
                    name = soup("span", class_="title-info-title-text").text
                except AttributeError:
                    name = None
                    logging.ERROR('Название не найдено!!!')
                try:
                    username = soup("span",
                                    class_="sticky-header-seller-text").text
                except AttributeError:
                    username = None
                try:
                    price = soup("span", class_="js-item-price").text
                    price = int(''.join(price.split()))
                except AttributeError:
                    price = None
                try:
                    street_address = soup("span",
                                          itemprop="streetAddress").text
                    street_address = street_address.replace('\n', ' ')
                except AttributeError:
                    street_address = 'г. Москва'
                try:
                    description = soup("div", class_="item-description").text
                    description = description.replace(';', ',')
                except AttributeError:
                    description = None
                    logging.error(f'Описание не найдено:{site}{link}')
                num = link.split('_')[-1]

                try:
                    url_pictures = soupAll(
                        "div", class_="js-gallery-extended-img-frame"
                                          )
                    for url_picture in url_pictures:
                        picture = url_picture['data-url']
                        picture_num = url_picture['data-image-id']
                        p = requests.get(f'https:{picture}')
                        path = 'webapp/templates/images/uploaded/'
                        with open(f'{path}{picture_num}.jpg', 'wb') as out:
                            out.write(p.content)
                            out.close()
                        pictures = {
                            'auto_id': num,
                            'url_picture': f'{picture_num}.jpg'
                                    }
                        url_full.append(pictures)
                except Exception:
                    logging.error('Ошибка IMAGE')
                    url_full.append({'auto_id': num,
                                     'url_picture': '1200.jpg'})
                logging.info('Картинки загружены')
                try:
                    params = {}
                    params_all = soupAll('li', class_="item-params-list-item")
                    for param in params_all:
                        param = param.text.replace('\n', '').split(':')
                        params['auto_id'] = num
                        par_tr = translate.get(param[0])
                        params[par_tr] = param[1].strip().replace(u'\xa0', u'')
                        for param_keys in param_fields:
                            params.setdefault(param_keys)
                except AttributeError:
                    params = None
                params_full.append(params)

                driver = webdriver.Chrome()

                driver.get(f"{site}{link}")
                button = driver.find_element_by_xpath(
                    """//a[@class='button item-phone-button
                    js-item-phone-button button-origin button-origin-blue
                    button-origin_full-width button-origin_large-extra
                    item-phone-button_hide-phone item-phone-button_card
                    js-item-phone-button_card']""")

                sleep(2)
                button.click()
                sleep(2)

                driver.save_screenshot('tel_scr.png')
                image = driver.find_element_by_xpath(
                    "//div[@class='popup-content']//*")
                location = image.location
                size = image.size
                image = Image.open('tel_scr.png')
                image = Image.open('tel_scr.png')
                x = location['x']-20
                y = location['y']-20
                width = size['width']+50
                height = size['height']+50

                image.crop((x, y, x+width, y+height)).save('tel.gif')

                img = Image.open('tel.gif')
                pytesseract.tesseract_cmd = r'''C:/
                    Program Files (x86)/Tesseract-OCR/tesseract'''
                number = image_to_string(img)[:17]
                number = number.replace(
                    ' ', '').replace('-', '').replace('\n', '')
                print(number)
                if re.fullmatch('[0-9]*', number) and number:
                    print(number)
                    driver.close()
                else:
                    image.crop((x, y, x+width+40, y+height+40)).save('tel.gif')

                    img = Image.open('tel.gif')
                    pytesseract.tesseract_cmd = r'''C:/
                        Program Files (x86)/Tesseract-OCR/tesseract'''
                    number = image_to_string(img)[:17]
                    number = number.replace(
                        ' ', '').replace('-', '').replace('\n', '')
                    print(number)
                    driver.close()

                user_info = {
                    'id': number[2:],
                    'name': username,
                    'street_address': street_address,
                    'number': number,
                    'role': 'user'
                }
                print(user_info)
                result = {
                    'id': num,
                    'name': name,
                    'price': price,
                    'description': description,
                    'user_id': number[2:],
                    'active': True
                        }
                print(result)
            results.append(result)
            users_info.append(user_info)
        return results
        return url_full
        return params_full
        return users_info
        logging.info(f'Данные получены')
    except Exception:
        logging.warning('Программа завершена с ошибкой!')


def download_to_csv():
    for index in range(0, 4):
        with open(csv_names[index], 'a', encoding='utf-8', newline='') as f:
            logging.info('Записываю в таблицу')
            writer = csv.DictWriter(f, fields[index], delimiter=';')
            writer.writeheader()
            writer.writerows(material[index])
            logging.info(f'Данные записаны в таблицу')


def download_to_db():
    with open('users.csv', 'r', encoding='utf-8') as f:
        conn = create_engine(SQLALCHEMY_DATABASE_URI).raw_connection()
        cursor = conn.cursor()
        cmd = """COPY users(id, name, street_address,
                           number, role) FROM STDIN WITH (FORMAT CSV,
                                        HEADER TRUE, DELIMITER ';');"""
        cursor.copy_expert(cmd, f)
        conn.commit()
    with open('auto.csv', 'r', encoding='utf-8') as f:
        conn = create_engine(SQLALCHEMY_DATABASE_URI).raw_connection()
        cursor = conn.cursor()
        cmd = """COPY auto(id, name, price,
                           description, user_id,
                           active, brand_id,
                           model_id) FROM STDIN WITH (FORMAT CSV,
                                        HEADER TRUE, DELIMITER ';');"""
        cursor.copy_expert(cmd, f)
        conn.commit()
    with open('auto_img.csv', 'r', encoding='utf-8') as f:
        conn = create_engine(SQLALCHEMY_DATABASE_URI).raw_connection()
        cursor = conn.cursor()
        cmd = """COPY images(auto_id, url_picture) FROM STDIN WITH (FORMAT CSV,
                                        HEADER TRUE, DELIMITER ';');"""
        cursor.copy_expert(cmd, f)
        conn.commit()
    with open('auto_params.csv', 'r', encoding='utf-8') as f:
        conn = create_engine(SQLALCHEMY_DATABASE_URI).raw_connection()
        cursor = conn.cursor()
        cmd = """COPY params(auto_id, holders, generation, condition,
        steering_wheel,wheeldrive,
        color, engine_capacity, model, mileage, brand, year,
        body_type, type_engine, gear, power, doors, vin,
        location, equipment, modification) FROM STDIN WITH (FORMAT CSV,
                                        HEADER TRUE, DELIMITER ';');"""
        cursor.copy_expert(cmd, f)
        conn.commit()


if __name__ == "__main__":
    get_links_from_pages()
    get_link_info()
    download_to_csv()
    download_to_db()
