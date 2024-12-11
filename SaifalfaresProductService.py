import time

import pymysql
from selenium import webdriver
import json
from selenium.webdriver.common.by import By
from urllib.parse import quote

import SaifalfaresConfig

chrome_driver_instance = None


def getDatabaseConnection4Saifalfares():
    mysqlConn4Fak = pymysql.connect(host=SaifalfaresConfig.saifalfaresConfig['saifalfares']['db']['host'],
                                    port=SaifalfaresConfig.saifalfaresConfig['saifalfares']['db']['port'],
                                    user=SaifalfaresConfig.saifalfaresConfig['saifalfares']['db']['user'],
                                    password=SaifalfaresConfig.saifalfaresConfig['saifalfares']['db']['pass'],
                                    database=SaifalfaresConfig.saifalfaresConfig['saifalfares']['db']['dbName'])

    return mysqlConn4Fak


def getCookie(_userName):
    cookie = open(SaifalfaresConfig.saifalfaresConfig['saifalfares']['cookieDir'] +
                  str(_userName) + ".cookie", 'r')
    cookie_str = cookie.read()
    cookie.close()

    return cookie_str


def createChromeDriver(cookieName):
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        chrome_driver_instance = webdriver.Chrome()

        chrome_driver_instance.get("https://saifalfares.com/")

        time.sleep(1)

        chrome_driver_instance.delete_all_cookies()

        cookie_str = getCookie(cookieName)
        if cookie_str is None:
            print("加载cookie失败," + cookieName)

            return

        cookies = json.loads(cookie_str)

        for c in cookies:
            chrome_driver_instance.add_cookie(c)

        chrome_driver_instance.refresh()
    except Exception as e:
        print(e.__str__())


def insert(_description, _category, _title, _image, _price):
    try:
        _connection = getDatabaseConnection4Saifalfares()

        _cursor = _connection.cursor()

        _cursor.execute("insert into saifalfares_Product_scrapy(title, price, description, images, category) "
                        "values ('" + quote(_title) + "', '" +
                        _price + "', '" + quote(_description) + "', '" + _image + "', '" + _category + "')")

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


def handleProductDetail(_url):
    chrome_driver_instance.get(_url)

    time.sleep(2)

    title = chrome_driver_instance.find_element(By.XPATH, "//h1[@class='productView-title']/span").text
    print(title)

    price = chrome_driver_instance.find_element(By.XPATH, "//div[contains(@class, 'productView-price')]/div").text
    print(price)

    description = chrome_driver_instance.find_element(By.XPATH, "//div[@id='tab-description-mobile']").text
    print(description)

    images = chrome_driver_instance.find_elements(By.XPATH, "//div[contains(@class, 'productView-image')]//img")
    for image in images:
        print(image.get_attribute('src'))


def listProducts(_url, _userName, _category):
    global chrome_driver_instance

    try:
        createChromeDriver(_userName)

        total = SaifalfaresConfig.saifalfaresConfig['saifalfares']['totalPages']
        count = SaifalfaresConfig.saifalfaresConfig['saifalfares']['begin']
        detailUrls = []
        while count <= total:
            actualUrl = _url + "?page=" + str(count)

            chrome_driver_instance.get(actualUrl)

            time.sleep(2)

            urls = chrome_driver_instance.find_elements(By.XPATH, "//li//a[contains(@class, 'card-title')]")
            for url in urls:
                if url.get_attribute('href'):
                    detailUrls.append(url.get_attribute('href'))

            count = count + 1

        index = 0
        for productDetailUrl in detailUrls:
            handleProductDetail(productDetailUrl)
            index = index + 1

    except Exception as e:
        print(e.__str__)
    finally:
        if chrome_driver_instance:
            chrome_driver_instance.close()


if __name__ == '__main__':
    listProducts(SaifalfaresConfig.saifalfaresConfig['saifalfares']['initUrl'],
                 SaifalfaresConfig.saifalfaresConfig['saifalfares']['userName'],
                 SaifalfaresConfig.saifalfaresConfig['saifalfares']['category'])
