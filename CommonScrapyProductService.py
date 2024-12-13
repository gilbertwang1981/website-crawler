import time

import pymysql
from selenium import webdriver
from urllib.parse import quote

import CommonScrapyConfig
from AtcacarScrapy import AtcacarScrapy

chrome_driver_instance = None


def getDatabaseConnection():
    mysqlConnection = pymysql.connect(
        host=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['host'],
        port=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['port'],
        user=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['user'],
        password=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['pass'],
        database=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['dbName'])

    return mysqlConnection


def insert(_category, _title, _image, _description, _price):
    try:
        _connection = getDatabaseConnection()

        _cursor = _connection.cursor()

        _cursor.execute("insert into common_product_scrapy(title, images, category, description, price) "
                        "values ('" + quote(_title) + "', '"
                        + _image + "', '" + _category + "', '" + quote(_description) + "', '" + _price + "')")

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


def listCategories(scrapy):
    try:
        chrome_driver_instance.get(CommonScrapyConfig.commonScrapyConfig['scrapy']['initUrl'])

        time.sleep(1)

        categoryUrls = scrapy.getProductListByCategories()

        return categoryUrls
    except Exception as e:
        print(e.__str__())
        return []


def scrapyProductDetail(_url, scrapy):
    chrome_driver_instance.get(_url)

    time.sleep(1)

    detail = scrapy.getProductDetail()

    title = detail['title']
    description = detail['description']
    imageUrl = detail['image']
    price = detail['price']
    category = CommonScrapyConfig.commonScrapyConfig['scrapy']['category']

    insert(category, title, imageUrl, description, price)


def traverseProductList(url, scrapy):
    chrome_driver_instance.get(url)

    time.sleep(1)

    urls = scrapy.getProductDetailByList()

    for _url in urls:
        scrapyProductDetail(_url, scrapy)


def listProducts(scrapy):
    categories = listCategories(scrapy)
    for category in categories:
        traverseProductList(category, scrapy)


def getChromeDriver():
    return chrome_driver_instance


def closeChromeDriver():
    chrome_driver_instance.close()
