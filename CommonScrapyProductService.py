import time

import pymysql
from selenium import webdriver
from urllib.parse import quote

import CommonScrapyConfig

chrome_driver_instance = None


def getDatabaseConnection():
    mysqlConnection = pymysql.connect(
        host=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['host'],
        port=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['port'],
        user=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['user'],
        password=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['pass'],
        database=CommonScrapyConfig.commonScrapyConfig['scrapy']['db']['dbName'])

    return mysqlConnection


def getProductListPageSize():
    return CommonScrapyConfig.commonScrapyConfig['scrapy']['pageSize']


def insert(_category, _title, _image, _description, _price, _sku):
    try:
        _connection = getDatabaseConnection()

        _cursor = _connection.cursor()

        _cursor.execute("insert into common_product_scrapy(title, images, category, description, price, sku) "
                        "values ('" + quote(_title) + "', '"
                        + _image + "', '" + _category + "', '" + quote(_description) + "', '" + _price + "', '" + _sku + "')")

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
    sku = detail['sku']

    if not title or not imageUrl:
        print("关键字段(标题)为空不插入，可能正在被风控。")
    else:
        insert(category, title, imageUrl, description, price, sku)


def traverseProductList(url, scrapy, page, pageSize):
    schema = CommonScrapyConfig.commonScrapyConfig['scrapy']['pageSchema']

    targetUrl = url + schema + str(page)

    print("READY TO SCRAPY - " + targetUrl)

    chrome_driver_instance.get(targetUrl)

    time.sleep(1)

    _urls = scrapy.getProductDetailByList()

    for _url in _urls:
        scrapyProductDetail(_url, scrapy)

    if len(_urls) < pageSize:
        return

    traverseProductList(url, scrapy, page + 1, pageSize)


def listProducts(scrapy, pageSize):
    categories = listCategories(scrapy)
    begin = CommonScrapyConfig.commonScrapyConfig['scrapy']['beginPage']
    for category in categories:
        traverseProductList(category, scrapy, begin, pageSize)


def closeChromeDriver():
    chrome_driver_instance.close()
