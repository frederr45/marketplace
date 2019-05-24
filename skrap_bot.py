from selenium import webdriver

from time import sleep
from PIL import Image
from pytesseract import image_to_string, pytesseract


class Bot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.navigate()

    def take_screenshot(self):
        self.driver.save_screenshot('tel_scr.png')

    def crop(self, location, size):
        image = Image.open('tel_scr.png')
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        image.crop((x, y, x+width, y+height)).save('tel.gif')

        self.tel_recon()

    def tel_recon(self):
        img = Image.open('tel.gif') 
        pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        number = image_to_string(img)
        print(number[:17])
        

    def navigate(self):
        self.driver.get('https://www.avito.ru/moskva/avtomobili/renault_grand_scenic_2008_1349010379')
        button = self.driver.find_element_by_xpath("//a[@class='button item-phone-button js-item-phone-button button-origin button-origin-blue button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card']")
        button.click()
        sleep(1)
        self.take_screenshot()

        image = self.driver.find_element_by_xpath("//div[@class='popup-content']//*")
        location = image.location
        size = image.size

        self.crop(location, size)


def numbers():
    b = Bot()


if __name__ == '__main__':
    numbers()
    
    
    
