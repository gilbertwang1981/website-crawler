import time
from bs4 import BeautifulSoup
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

import SanfordjapanConfig

chrome_driver_instance = None


def getDatabaseConnection():
    mysqlConnection = pymysql.connect(host=SanfordjapanConfig.sanfordjapanConfig['sanfordjapan']['db']['host'],
                                      port=SanfordjapanConfig.sanfordjapanConfig['sanfordjapan']['db']['port'],
                                      user=SanfordjapanConfig.sanfordjapanConfig['sanfordjapan']['db']['user'],
                                      password=SanfordjapanConfig.sanfordjapanConfig['sanfordjapan']['db']['pass'],
                                      database=SanfordjapanConfig.sanfordjapanConfig['sanfordjapan']['db']['dbName'])

    return mysqlConnection


def createChromeDriver():
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        chrome_driver_instance = webdriver.Chrome()

        chrome_driver_instance.get("https://sanfordjapan.com/index.html")

        time.sleep(1)

    except Exception as e:
        print(e.__str__())


def insert(_category, _title, _image, _description):
    try:
        _connection = getDatabaseConnection()

        _cursor = _connection.cursor()

        _cursor.execute("insert into common_product_scrapy(title, images, category, description) "
                        "values ('" + quote(_title) + "', '"
                        + _image + "', '" + _category + "', '" + quote(_description) + "')")

        _connection.commit()

    except Exception as e:
        print(e.__str__())
        if _connection:
            _connection.rollback()
    finally:
        if _cursor:
            _cursor.close()
        if _connection:
            _connection.close()


def listProducts(_url, _category):
    global chrome_driver_instance

    try:
        createChromeDriver()

        categories = chrome_driver_instance.find_elements(By.XPATH, "//div[@id='cssmenu']"
                                                                    "/ul"
                                                                    "/li"
                                                                    "/a")
        categoryUrls = []
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        productListUrls = []
        for categoryUrl in categoryUrls:
            chrome_driver_instance.get(categoryUrl)
            time.sleep(2)
            productLists = chrome_driver_instance.find_elements(By.XPATH, "//div[@class='maininpro']"
                                                                          "//li"
                                                                          "/a")
            for productList in productLists:
                productListUrls.append(productList.get_attribute('href'))

            productListUrls = list(set(productListUrls))

        for productListUrl in productListUrls:
            chrome_driver_instance.get(productListUrl)
            time.sleep(2)
            details = chrome_driver_instance.find_elements(By.XPATH, "//div[@class='mainin']"
                                                                     "/ul"
                                                                     "/li"
                                                                     "/a")
            imagePrefix = productListUrl[:productListUrl.rfind('/')]

            for detail in details:
                title = ''
                description = ''
                imageUrl = ''
                try:
                    title = BeautifulSoup(detail.get_attribute('data-title'), 'html.parser').get_text()
                except Exception as e:
                    e.__str__()
                try:
                    description = BeautifulSoup(detail.get_attribute('data-description'), 'html.parser').get_text()
                except Exception as e:
                    e.__str__()
                try:
                    imageUrl = imagePrefix + "/" + detail.get_attribute('data-largesrc')
                except Exception as e:
                    e.__str__()

                categoryName = SanfordjapanConfig.sanfordjapanConfig['sanfordjapan']['category']

                print(title + "\n" + imageUrl + "\n" + description + "\n")

                insert(categoryName, title, imageUrl, description)
    except Exception as e:
        print(e.__str__)
    finally:
        if chrome_driver_instance:
            chrome_driver_instance.close()


if __name__ == '__main__':
    listProducts(SanfordjapanConfig.sanfordjapanConfig['sanfordjapan']['initUrl'],
                 SanfordjapanConfig.sanfordjapanConfig['sanfordjapan']['category'])
