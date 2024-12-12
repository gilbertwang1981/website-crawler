import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

import VictorwatchConfig

chrome_driver_instance = None


def getDatabaseConnection4Victorwatch():
    mysqlConn4Victorwatch = pymysql.connect(host=VictorwatchConfig.victorwatchConfig['victorwatch']['db']['host'],
                                            port=VictorwatchConfig.victorwatchConfig['victorwatch']['db']['port'],
                                            user=VictorwatchConfig.victorwatchConfig['victorwatch']['db']['user'],
                                            password=VictorwatchConfig.victorwatchConfig['victorwatch']['db']['pass'],
                                            database=VictorwatchConfig.victorwatchConfig['victorwatch']['db']['dbName'])

    return mysqlConn4Victorwatch


def createChromeDriver():
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        chrome_driver_instance = webdriver.Chrome()

        chrome_driver_instance.get("https://victorwatch.com/")

        time.sleep(1)

    except Exception as e:
        print(e.__str__())


def insert(_category, _title, _image, _price):
    try:
        _connection = getDatabaseConnection4Victorwatch()

        _cursor = _connection.cursor()

        _cursor.execute("insert into victorwatch_product_scrapy(title, images, category, price) "
                        "values ('" + quote(_title) + "', '"
                        + _image + "', '" + _category + "', '" + _price + "')")

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


def handleProductDetail(_url, _category):
    chrome_driver_instance.get(_url)

    time.sleep(1)

    title = chrome_driver_instance.find_element(By.XPATH,
                                                "//div[@class='product__title']/h1").text

    price = chrome_driver_instance.find_element(By.XPATH,
                                                "//div[@class='price__sale']"
                                                "//span[contains(@class, 'price-item')]").text
    if not price:
        price = chrome_driver_instance.find_element(By.XPATH,
                                                    "//div[@class='price__regular']"
                                                    "//span[contains(@class, 'price-item')]").text

    image = chrome_driver_instance.find_element(By.XPATH,
                                                "//li[contains(@class, 'product__media-item')]"
                                                "//div[contains(@class, 'product__media')]/img").get_attribute('src')
    image = image[:image.find('?')]

    insert(_category, title, image, price)


def listProducts(_url, _category):
    global chrome_driver_instance

    try:
        createChromeDriver()

        total = VictorwatchConfig.victorwatchConfig['victorwatch']['totalPages']
        count = VictorwatchConfig.victorwatchConfig['victorwatch']['begin']
        detailUrls = []
        while count <= total:
            actualUrl = _url + "?page=" + str(count)

            chrome_driver_instance.get(actualUrl)

            time.sleep(2)

            urls = chrome_driver_instance.find_elements(By.XPATH, "//div[@class='card__information']//a")
            for url in urls:
                if url.get_attribute('href'):
                    detailUrls.append(url.get_attribute('href'))

            count = count + 1

        index = 0
        detailUrls = list(set(detailUrls))
        for productDetailUrl in detailUrls:
            handleProductDetail(productDetailUrl, _category)
            index = index + 1

    except Exception as e:
        print(e.__str__)
    finally:
        if chrome_driver_instance:
            chrome_driver_instance.close()


if __name__ == '__main__':
    listProducts(VictorwatchConfig.victorwatchConfig['victorwatch']['initUrl'],
                 VictorwatchConfig.victorwatchConfig['victorwatch']['category'])
