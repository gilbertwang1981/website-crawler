import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

import FarookonlineConfig

chrome_driver_instance = None


def getDatabaseConnection():
    mysqlConn = pymysql.connect(host=FarookonlineConfig.farookonlineConfig['farookonline']['db']['host'],
                                port=FarookonlineConfig.farookonlineConfig['farookonline']['db']['port'],
                                user=FarookonlineConfig.farookonlineConfig['farookonline']['db']['user'],
                                password=FarookonlineConfig.farookonlineConfig['farookonline']['db']['pass'],
                                database=FarookonlineConfig.farookonlineConfig['farookonline']['db']['dbName'])

    return mysqlConn


def createChromeDriver():
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        chrome_driver_instance = webdriver.Chrome()

        chrome_driver_instance.get(FarookonlineConfig.farookonlineConfig['farookonline']['initUrl'])

        time.sleep(1)

    except Exception as e:
        e.__str__()


def loadingProductList():
    c = 0
    total = FarookonlineConfig.farookonlineConfig['farookonline']['clicks']
    while c < total:
        time.sleep(3)

        try:
            chrome_driver_instance.find_element(By.XPATH, "//button[@class='show-more-btn hover-btn']").click()
        except Exception as e:
            e.__str__()

        c = c + 1

    detailUrls = []
    details = chrome_driver_instance.find_elements(By.XPATH, "//div[@class='product-item']"
                                                             "/a")
    for detail in details:
        detailUrls.append(detail.get_attribute('href'))

    print(len(detailUrls))

    return detailUrls


def detailProduct(_url):
    try:
        chrome_driver_instance.get(_url)

        time.sleep(3)

        category = FarookonlineConfig.farookonlineConfig['farookonline']['category']

        title = ''
        description = ''
        price = ''
        imageUrls = []

        try:
            title = chrome_driver_instance.find_element(By.XPATH,
                                                        "//div[@class='all-product-grid']"
                                                        "//div[@class='product-dt-view']"
                                                        "//div[@class='product-dt-right']"
                                                        "/h2").text
        except Exception as e:
            e.__str__()

        try:
            price = chrome_driver_instance.find_element(By.XPATH,
                                                        "//div[@class='main-price ']"
                                                        "/span").text
            price = price.split(' ')[1]
        except Exception as e:
            e.__str__()

        try:
            images = chrome_driver_instance.find_elements(By.XPATH,
                                                          "//div[contains(@class, 'gallery-thumbs')]"
                                                          "/div"
                                                          "/img")
            for image in images:
                imageUrls.append(image.get_attribute('src'))
        except Exception as e:
            e.__str__()

        try:
            description = chrome_driver_instance.find_element(By.XPATH, "//div[@id='myTabContent']"
                                                                        "//div[@class='pdct-dt-step']").text
        except Exception as e:
            e.__str__()

        _connection = getDatabaseConnection()

        _cursor = _connection.cursor()

        _cursor.execute("insert into common_product_scrapy(title, price, description, images, category) "
                        "values ('" + quote(title) + "', '" +
                        str(price) + "', '" + quote(description) + "', '" + ','.join(imageUrls) + "', '" + category + "')")

        _connection.commit()

    except Exception as e:
        e.__str__()
        if _connection:
            _connection.rollback()
    finally:
        if _cursor:
            _cursor.close()
        if _connection:
            _connection.close()


def listProducts():
    global chrome_driver_instance

    try:
        createChromeDriver()

        urls = loadingProductList()
        for detailUrl in urls:
            detailProduct(detailUrl)

    except Exception as e:
        print(e.__str__)
    finally:
        if chrome_driver_instance:
            chrome_driver_instance.close()


if __name__ == '__main__':
    listProducts()
