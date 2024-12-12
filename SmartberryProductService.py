import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

import SmartberryConfig

chrome_driver_instance = None


def getDatabaseConnection4Smartberry():
    mysqlConn4Smartberry = pymysql.connect(host=SmartberryConfig.smartberryConfig['smartberry']['db']['host'],
                                           port=SmartberryConfig.smartberryConfig['smartberry']['db']['port'],
                                           user=SmartberryConfig.smartberryConfig['smartberry']['db']['user'],
                                           password=SmartberryConfig.smartberryConfig['smartberry']['db']['pass'],
                                           database=SmartberryConfig.smartberryConfig['smartberry']['db']['dbName'])

    return mysqlConn4Smartberry


def createChromeDriver():
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        chrome_driver_instance = webdriver.Chrome()

        chrome_driver_instance.get("https://smartberry.com.cn/")

        time.sleep(1)

    except Exception as e:
        print(e.__str__())


def insert(_description, _category, _title, _image):
    try:
        _connection = getDatabaseConnection4Smartberry()

        _cursor = _connection.cursor()

        _cursor.execute("insert into smartberry_Product_scrapy(title, description, images, category) "
                        "values ('" + quote(_title) + "', '" + quote(_description) + "', '"
                        + _image + "', '" + _category + "')")

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
                                                "//div[@class='ly_product_purchase_2']"
                                                "//div[@class='goods_info']/h1").text

    description = chrome_driver_instance.find_element(By.XPATH,
                                                      "//div[@class='ly_product_purchase_2']"
                                                      "//div[@class='goods_info']"
                                                      "//div[contains(@class, 'g_desc')]").text

    urls = []
    images = chrome_driver_instance.find_elements(By.XPATH, "//li[@class='pic_box  ']/img")
    for image in images:
        s = image.get_attribute('data-srcset')
        if s:
            urls.append(s[2:s.find('?')])
    imageUrls = ','.join(urls)

    insert(description, _category, title, imageUrls)


def listProducts(_url, _category):
    global chrome_driver_instance

    try:
        createChromeDriver()

        total = SmartberryConfig.smartberryConfig['smartberry']['totalPages']
        count = SmartberryConfig.smartberryConfig['smartberry']['begin']
        detailUrls = []
        while count <= total:
            actualUrl = _url + "?page=" + str(count) + "&per-page=40"

            chrome_driver_instance.get(actualUrl)

            time.sleep(2)

            urls = chrome_driver_instance.find_elements(By.XPATH, "//div[@class='themes_prod']//a")
            for url in urls:
                if url.get_attribute('href'):
                    detailUrls.append(url.get_attribute('href'))

            count = count + 1

        index = 0
        for productDetailUrl in detailUrls:
            handleProductDetail(productDetailUrl, _category)
            index = index + 1

    except Exception as e:
        print(e.__str__)
    finally:
        if chrome_driver_instance:
            chrome_driver_instance.close()


if __name__ == '__main__':
    listProducts(SmartberryConfig.smartberryConfig['smartberry']['initUrl'],
                 SmartberryConfig.smartberryConfig['smartberry']['category'])
