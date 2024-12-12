import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

import HajsabbaghConfig

chrome_driver_instance = None


def getDatabaseConnection4Hajsabbagh():
    mysqlConn4Hajsabbagh = pymysql.connect(host=HajsabbaghConfig.hajsabbaghConfig['hajsabbagh']['db']['host'],
                                           port=HajsabbaghConfig.hajsabbaghConfig['hajsabbagh']['db']['port'],
                                           user=HajsabbaghConfig.hajsabbaghConfig['hajsabbagh']['db']['user'],
                                           password=HajsabbaghConfig.hajsabbaghConfig['hajsabbagh']['db']['pass'],
                                           database=HajsabbaghConfig.hajsabbaghConfig['hajsabbagh']['db']['dbName'])

    return mysqlConn4Hajsabbagh


def insert(_category, _title, _image, _price, _description):
    try:
        _connection = getDatabaseConnection4Hajsabbagh()

        _cursor = _connection.cursor()

        _cursor.execute("insert into hajsabbagh_product_scrapy(title, images, category, price, description) "
                        "values ('" + quote(_title) + "', '"
                        + _image + "', '" + _category + "', '" + _price + "', '" + quote(_description) + "')")

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


def createChromeDriver():
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        chrome_driver_instance = webdriver.Chrome()

    except Exception as e:
        print(e.__str__())


def listCategories():
    try:
        chrome_driver_instance.get(HajsabbaghConfig.hajsabbaghConfig['hajsabbagh']['initUrl'])

        time.sleep(1)

        productListUrls = chrome_driver_instance.find_elements(By.XPATH, "//li[@id='menu-item-21614']//a[@href]")
        categoryUrls = []
        for productListUrl in productListUrls:
            if not productListUrl.get_attribute('href').endswith('#'):
                categoryUrls.append(productListUrl.get_attribute('href'))

        return categoryUrls
    except Exception as e:
        print(e.__str__())
        return []


def scrapyProductDetail(_url):
    chrome_driver_instance.get(_url)

    time.sleep(1)

    title = ''
    description = ''
    price = ''
    imageUrl = ''

    try:
        title = chrome_driver_instance.find_element(By.XPATH, "//h1[contains(@class, 'product_title')]").text
    except Exception as e:
        e.__str__()

    try:
        price = chrome_driver_instance.find_element(By.XPATH, "//p[@class='price']"
                                                              "//span[contains(@class, "
                                                              "'woocommerce-Price-amount')]").text
        price = price[len("AED"):]
    except Exception as e:
        e.__str__()

    try:
        description = chrome_driver_instance.find_element(By.XPATH, "//div["
                                                                    "contains(@class, "
                                                                    "'woocommerce-Tabs-panel--description')]").text
    except Exception as e:
        e.__str__()

    try:
        image = chrome_driver_instance.find_element(By.XPATH, "//div[@class='woocommerce-product-gallery__wrapper']"
                                                              "//img")
        if image:
            imageUrl = image.get_attribute("src")
    except Exception as e:
        e.__str__()

    category = HajsabbaghConfig.hajsabbaghConfig['hajsabbagh']['category']
    insert(category,
           title, imageUrl, price, description)


def traverseProductList(url, page):
    chrome_driver_instance.get(url + "page/" + str(page) + "/")

    time.sleep(1)

    detailUrls = chrome_driver_instance.find_elements(By.XPATH, "//ul[contains(@class, 'product')]"
                                                                "/li[contains(@class, 'product')]/a")

    urls = []
    for detailUrl in detailUrls:
        if "add-to-cart" not in detailUrl.get_attribute('href'):
            urls.append(detailUrl.get_attribute('href'))

    for url in urls:
        scrapyProductDetail(url)

    if len(detailUrls) < 20:
        return

    traverseProductList(url, page + 1)


def listProducts():
    categories = listCategories()
    for category in categories:
        traverseProductList(category, 1)


if __name__ == '__main__':
    createChromeDriver()

    listProducts()

    chrome_driver_instance.close()
