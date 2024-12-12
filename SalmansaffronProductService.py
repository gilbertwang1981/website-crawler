import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

import SalmansaffronConfig

chrome_driver_instance = None


def getDatabaseConnection4Salmansaffron():
    mysqlConn4Salmansaffron = pymysql.connect(
        host=SalmansaffronConfig.salmansaffronConfig['salmansaffron']['db']['host'],
        port=SalmansaffronConfig.salmansaffronConfig['salmansaffron']['db']['port'],
        user=SalmansaffronConfig.salmansaffronConfig['salmansaffron']['db']['user'],
        password=SalmansaffronConfig.salmansaffronConfig['salmansaffron']['db']['pass'],
        database=SalmansaffronConfig.salmansaffronConfig['salmansaffron']['db']['dbName'])

    return mysqlConn4Salmansaffron


def insert(_category, _title, _image, _price, _description):
    try:
        _connection = getDatabaseConnection4Salmansaffron()

        _cursor = _connection.cursor()

        _cursor.execute("insert into salmansaffron_product_scrapy(title, images, category, price, description) "
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
        chrome_driver_instance.get(SalmansaffronConfig.salmansaffronConfig['salmansaffron']['initUrl'])

        time.sleep(1)

        productListUrls = chrome_driver_instance.find_elements(By.XPATH, "//li[@class='elementor-icon-list-item']"
                                                                         "//a[@href]")
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
    price = ''
    imageUrl = ''

    try:
        title = chrome_driver_instance.find_element(By.XPATH, "//h2[contains(@class, 'product_title')]").text
    except Exception as e:
        e.__str__()

    try:
        price = chrome_driver_instance.find_element(By.XPATH, "//p[@class='price']"
                                                              "//span[contains(@class, "
                                                              "'woocommerce-Price-amount')]").text
        price = price[:-3]
    except Exception as e:
        e.__str__()

    try:
        desc = chrome_driver_instance.find_elements(By.XPATH, "//div[@data-elementor-type='product']"
                                                              "//div[contains(@class, 'elementor-column')][1]"
                                                              "//div[contains(@class, 'elementor-widget-container')]")
        if desc:
            description = desc[4].text
    except Exception as e:
        e.__str__()

    try:
        image = chrome_driver_instance.find_element(By.XPATH, "//div[@class='woocommerce-product-gallery__wrapper']"
                                                              "//img")
        if image:
            imageUrl = image.get_attribute("src")
    except Exception as e:
        e.__str__()

    category = SalmansaffronConfig.salmansaffronConfig['salmansaffron']['category']
    insert(category,
           title, imageUrl, price, description)


def traverseProductList(url):
    chrome_driver_instance.get(url)

    time.sleep(1)

    detailUrls = chrome_driver_instance.find_elements(By.XPATH, "//li[contains(@class, 'product')]/a[@href]")

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
