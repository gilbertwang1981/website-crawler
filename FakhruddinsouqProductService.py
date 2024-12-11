import time

import pymysql
from selenium import webdriver
import json
from selenium.webdriver.common.by import By
from urllib.parse import quote

import FakhruddinsouqConfig

chrome_driver_instance = None


def getDatabaseConnection4Fak():
    mysqlConn4Fak = pymysql.connect(host=FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['db']['host'],
                                    port=FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['db']['port'],
                                    user=FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['db']['user'],
                                    password=FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['db']['pass'],
                                    database=FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['db']['dbName'])

    return mysqlConn4Fak


def getCookie(_userName):
    cookie = open(FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['cookieDir'] +
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

        chrome_driver_instance.get("https://www.fakhruddinsouq.com/")

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


def insert(_description, _category, _title, _image, _sku):
    try:
        _connection = getDatabaseConnection4Fak()

        _cursor = _connection.cursor()

        _cursor.execute("insert into fakhruddinsouq_Product_scrapy(title, sku, description, images, category) "
                        "values ('" + quote(_title) + "', '" +
                        _sku + "', '" + quote(_description) + "', '" + _image + "', '" + _category + "')")

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


def getProductDescription(_url):
    try:
        chrome_driver_instance.get(_url)

        productDesc = chrome_driver_instance.find_element(By.XPATH, "//div[@class='shrot_descr']").text
        productDesc = productDesc + chrome_driver_instance.find_element(By.XPATH, "//div[@class='static_attr']").text
        if productDesc is None or productDesc == '':
            return ''
        else:
            return productDesc
    except Exception as e:
        print(e.__str__())

        return ''


def listProducts(_url, _userName, _category):
    global chrome_driver_instance

    try:
        createChromeDriver(_userName)

        total = FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['totalPages']
        count = FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['begin']
        detailUrls = []
        titles = []
        skus = []
        images = []
        while count <= total:
            actualUrl = _url + "?p=" + str(count)

            chrome_driver_instance.get(actualUrl)

            time.sleep(2)

            _details = chrome_driver_instance.find_elements(By.XPATH,
                                                            "//a[contains(@class, 'product-item-link')]")

            _images = chrome_driver_instance.find_elements(By.XPATH,
                                                           "//img[@class='product-image-photo ']")

            _skus = chrome_driver_instance.find_elements(By.XPATH, "//span[contains(@class, 'skulist')]")

            for detail in _details:
                detailUrls.append(detail.get_attribute('href'))
                titles.append(detail.text)

            for sku in _skus:
                skus.append(sku.text.split(':')[1])

            for image in _images:
                images.append(image.get_attribute('src'))

            count = count + 1

        productsDesc = []
        for url in detailUrls:
            desc = getProductDescription(url)
            productsDesc.append(desc)

        count = 0
        while count < len(detailUrls):
            insert(productsDesc[count], _category,
                   titles[count], images[count], skus[count])

            count = count + 1

    except Exception as e:
        print(e.__str__)
    finally:
        if chrome_driver_instance:
            chrome_driver_instance.close()


if __name__ == '__main__':
    listProducts(FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['initUrl'],
                 FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['userName'],
                 FakhruddinsouqConfig.fakConfig['fakhruddinsouq']['category'])
