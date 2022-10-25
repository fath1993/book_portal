from django.core.management.base import BaseCommand

from book_portal.settings import DRIVER_PATH

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_fidibo_book():
    url = 'https://fidibo.com/category/literature/foreign-story-novel'
    options = Options()
    options.headless = True
    options.add_argument("--disable-javascript")
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(url)

    item_list = driver.find_element(By.ID, 'item_list')

    books = item_list.find_elements(By.TAG_NAME, 'div')

    i = 0
    for book in books:
        try:
            book_image_class_item_image = book.find_element(By.CLASS_NAME, 'item-image')
            book_href_tag_a = book_image_class_item_image.find_element(By.TAG_NAME, 'a')
            book_href = book_href_tag_a.get_attribute('href')
            book_image_tag_img = book_image_class_item_image.find_element(By.TAG_NAME, 'img')
            """
            for getting all attr from a tag we use a method like below:
            
            attrs = driver.execute_script(
                'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;',
                book_image_tag_img)
            print(attrs)
            """
            book_image_thumbnail = book_image_tag_img.get_attribute('data-original')
            book_title = book.find_element(By.CLASS_NAME, 'title-book')
            book_author = book.find_element(By.CLASS_NAME, 'author-names')

            print(book_href)
            print(book_title.text)
            print(book_author.text)
            print(book_image_thumbnail)

            print("---------" + str(i) + "----------")
            i += 1
        except:
            pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_fidibo_book()




