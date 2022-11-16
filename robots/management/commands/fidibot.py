import io
import os

import jdatetime
import requests
from PIL import Image
from django.core.management.base import BaseCommand

from book_portal.settings import DRIVER_PATH

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bookshelf.models import Person, Author, Interpreter, Book
from gallery.models import ImageGallery


def get_or_create_person(person_name):
    try:
        old_person = Person.objects.get(person_name=person_name)
        return old_person
    except:
        new_person = Person(
            person_name=person_name,
        )
        new_person.save()
        return new_person


def get_or_create_author(person_object):
    try:
        old_author = Author.objects.get(person=person_object)
        return old_author
    except:
        new_author = Author(
            person=person_object,
        )
        new_author.save()
        return new_author


def get_or_create_interpreter(person_object):
    try:
        old_interpreter = Interpreter.objects.get(person=person_object)
        return old_interpreter
    except:
        new_interpreter = Interpreter(
            person=person_object,
        )
        new_interpreter.save()
        return new_interpreter


def image_downloader(img_link, image_name):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.108 Safari/537.36 '
    }
    try:
        the_wallpaper_link_request = requests.get(img_link, headers=headers,
                                                  timeout=5, stream=True)
        filename = str(image_name) + str(".jpg")
        with Image.open(io.BytesIO(the_wallpaper_link_request.content)) as im:
            im.save(os.path.join('media', filename), "JPEG")
        new_image = ImageGallery(
            image_name=filename,
            image_alt=filename,
            image_src=os.path.join('', filename),
        )
        new_image.save()
        print("getting image done: " + filename)
        return new_image
    except Exception as e:
        print("getting image problem: " + str(e))


def get_or_create_book(title, author_object, interpreter_object, on_paper_image_link, summery):
    try:
        old_book = Book.objects.get(title=title)
        return old_book
    except:
        new_book = Book(
            title=title,
            on_paper_image=image_downloader(on_paper_image_link, title),
            summery=summery,
            date_of_publish=jdatetime.datetime.now(),
            language='Fa',
            ISBN='1234',
            number_of_pages=100,
            is_physical_available=True,
            is_published_on_site=True,

        )
        new_book.save()
        new_book.authors.add(author_object)
        new_book.interpreters.add(interpreter_object)
        new_book.is_published_on_site = True
        new_book.save()
        return new_book


def get_fidibo_book():
    url = 'http://www.ketabsarayetandis.com/Books.aspx?Id=10'
    options = Options()
    options.headless = True
    options.add_argument("--disable-javascript")
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver2 = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(url)

    item_list = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_DataList2')

    books = item_list.find_elements(By.TAG_NAME, 'a')

    for book in books:
        driver2.get(book.get_attribute('href'))
        title = driver2.find_element(By.ID, 'ctl00_ContentPlaceHolder1_DataList2_ctl00_Label1')
        author = driver2.find_element(By.ID, 'ctl00_ContentPlaceHolder1_DataList2_ctl00_Label3')
        interpreter = driver2.find_element(By.ID, 'ctl00_ContentPlaceHolder1_DataList2_ctl00_Label4')
        on_paper_image = driver2.find_element(By.ID, 'ctl00_ContentPlaceHolder1_DataList2_ctl00_Image1')
        summery_content = driver2.find_element(By.ID, 'ctl00_ContentPlaceHolder1_DataList2_ctl00_Label8')
        summery_all = summery_content.find_elements(By.TAG_NAME, 'span')
        summery = ''
        for sum in summery_all:
            summery += ' ' + str(sum.text)
        print(title.text)
        print(author.text)
        print(interpreter.text)
        print(on_paper_image.get_attribute('src'))
        print(summery)
        get_or_create_book(title.text, get_or_create_author(get_or_create_person(author.text)),
                           get_or_create_interpreter(get_or_create_person(interpreter.text)),
                           on_paper_image.get_attribute('src'), summery)


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_fidibo_book()
