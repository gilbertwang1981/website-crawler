import time
import json
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


def getCookie(_userName):
    cookie = open(CommonScrapyConfig.commonScrapyConfig['scrapy']['cookieDirectory'] + str(_userName) + ".cookie", 'r')
    cookie_str = cookie.read()
    cookie.close()

    return cookie_str


def loadingCookie(cookieName):
    chrome_driver_instance.delete_all_cookies()

    cookie_str = getCookie(cookieName)
    if cookie_str is None:
        print("加载cookie失败," + cookieName)

        return

    cookies = json.loads(cookie_str)

    for c in cookies:
        chrome_driver_instance.add_cookie(c)

    chrome_driver_instance.refresh()


def getProductListPageSize():
    return CommonScrapyConfig.commonScrapyConfig['scrapy']['pageSize']


def insert(_category, _title, _image, _description, _price, _sku):
    try:
        _connection = getDatabaseConnection()

        _cursor = _connection.cursor()

        _cursor.execute("insert into common_product_scrapy(title, images, category, description, price, sku) "
                        "values ('" + quote(_title) + "', '"
                        + _image + "', '" + _category + "', '" + quote(_description) +
                        "', '" + _price + "', '" + _sku + "')")

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

        loadingC = CommonScrapyConfig.commonScrapyConfig['scrapy']['loadingCookie']
        if loadingC == 1:
            chrome_driver_instance.get(CommonScrapyConfig.commonScrapyConfig['scrapy']['loadingCookieUrl'])

            time.sleep(1)

            userName = CommonScrapyConfig.commonScrapyConfig['scrapy']['userName']

            loadingCookie(userName)
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


def scrollingPage():
    enable = CommonScrapyConfig.commonScrapyConfig['scrapy']['scrolling']
    if enable == 0:
        return

    c = 0
    off = CommonScrapyConfig.commonScrapyConfig['scrapy']['scrollingOffset']
    totalTimes = CommonScrapyConfig.commonScrapyConfig['scrapy']['scrollingTimes']
    duration = CommonScrapyConfig.commonScrapyConfig['scrapy']['scrollingDuration']
    while c < totalTimes:
        off = off + c * 3000
        chrome_driver_instance.execute_script("window.scrollBy(0," + str(off) + ")")

        time.sleep(duration)

        c = c + 1


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

    if not title:
        print("关键字段(标题)为空不插入，可能正在被风控。")
    else:
        insert(category, title, imageUrl, description, price, sku)


def traverseProductList(url, scrapy, page, pageSize):
    schema = CommonScrapyConfig.commonScrapyConfig['scrapy']['pageSchema']

    targetUrl = url + schema + str(page)

    print("READY TO SCRAPY - " + targetUrl)

    chrome_driver_instance.get(targetUrl)

    time.sleep(1)

    scrollingPage()

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
