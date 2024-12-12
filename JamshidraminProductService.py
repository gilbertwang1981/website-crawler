import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

import JamshidraminConfig

chrome_driver_instance = None


def getDatabaseConnection4Jamshidramin():
    mysqlConn4jamshidramin = pymysql.connect(
        host=JamshidraminConfig.jamshidraminConfig['jamshidramin']['db']['host'],
        port=JamshidraminConfig.jamshidraminConfig['jamshidramin']['db']['port'],
        user=JamshidraminConfig.jamshidraminConfig['jamshidramin']['db']['user'],
        password=JamshidraminConfig.jamshidraminConfig['jamshidramin']['db']['pass'],
        database=JamshidraminConfig.jamshidraminConfig['jamshidramin']['db']['dbName'])

    return mysqlConn4jamshidramin


def insert(_category, _title, _image, _description):
    try:
        _connection = getDatabaseConnection4Jamshidramin()

        _cursor = _connection.cursor()

        _cursor.execute("insert into jamshidramin_product_scrapy(title, images, category, description) "
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
        chrome_driver_instance.get(JamshidraminConfig.jamshidraminConfig['jamshidramin']['initUrl'])

        time.sleep(1)

        productListUrls = chrome_driver_instance.find_elements(By.XPATH, "//ul[@id='navbar']/li[3]/ul/li/a")
        categoryUrls = []
        for productListUrl in productListUrls:
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
    imageUrl = ''

    try:
        title = chrome_driver_instance.find_element(By.XPATH, "//div[@class='product-name']").text
    except Exception as e:
        e.__str__()

    try:
        description = chrome_driver_instance.find_element(By.XPATH, "//div[@class='options']").text
    except Exception as e:
        print(e.__str__())

    try:
        imageUrl = chrome_driver_instance.find_element(By.XPATH, "//img[@class='zoom-images']").get_attribute("src")
    except Exception as e:
        e.__str__()

    category = JamshidraminConfig.jamshidraminConfig['jamshidramin']['category']
    insert(category,
           title, imageUrl, description)


def traverseProductList(url):
    chrome_driver_instance.get(url)

    time.sleep(1)

    detailUrls = chrome_driver_instance.find_elements(By.XPATH, "//div[contains(@class, 'product')]/a[@href]")

    urls = []
    for detailUrl in detailUrls:
        urls.append(detailUrl.get_attribute('href'))

    for _url in urls:
        scrapyProductDetail(_url)


def listProducts():
    categories = listCategories()
    for category in categories:
        traverseProductList(category)


if __name__ == '__main__':
    createChromeDriver()

    listProducts()

    chrome_driver_instance.close()
