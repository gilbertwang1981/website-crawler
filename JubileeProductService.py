import time

import pymysql
from selenium import webdriver
import json
from selenium.webdriver.common.by import By
from urllib.parse import quote

import JubileeConfig

chrome_driver_instance = None


def getDatabaseConnection4Jubilee():
    mysqlConn4Jubilee = pymysql.connect(host=JubileeConfig.jubileeConfig['jubilee']['db']['host'],
                                        port=JubileeConfig.jubileeConfig['jubilee']['db']['port'],
                                        user=JubileeConfig.jubileeConfig['jubilee']['db']['user'],
                                        password=JubileeConfig.jubileeConfig['jubilee']['db']['pass'],
                                        database=JubileeConfig.jubileeConfig['jubilee']['db']['dbName'])

    return mysqlConn4Jubilee


def getCookie(_userName):
    cookie = open(JubileeConfig.jubileeConfig['jubilee']['cookieDir'] + str(_userName) + ".cookie", 'r')
    cookie_str = cookie.read()
    cookie.close()

    return cookie_str


def createChromeDriver(cookieName):
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        chrome_driver_instance = webdriver.Chrome()

        chrome_driver_instance.get("https://jubilee.ae/")

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


def preLoading():
    c = 0
    off = 2000
    while c < 15:
        off = off + c * 3000
        chrome_driver_instance.execute_script("window.scrollBy(0," + str(off) + ")")

        time.sleep(1)

        c = c + 1


def detailProduct(_url, _category):
    try:
        chrome_driver_instance.get(_url)
        time.sleep(3)

        try:
            title = chrome_driver_instance.find_element(By.XPATH,
                                                        "//div[contains(@class, 'ProductMeta')]"
                                                        "//h1[contains(@class, 'ProductMeta__Title')]").text
        except Exception as e:
            print("找不到title， " + e.__str__())

        try:
            price = chrome_driver_instance.find_elements(By.XPATH,
                                                         "//div[contains(@class, 'ProductMeta')]"
                                                         "//span[contains(@class, 'ProductMeta__Price')]")[0].text
        except Exception as e:
            print("找不到price， " + e.__str__())

        try:
            image = chrome_driver_instance.find_element(By.XPATH,
                                                        "//div[contains(@class, 'Product__Wrapper')]"
                                                        "//img[contains(@class, 'Image--fadeIn')]"). \
                get_attribute('data-srcset')
        except Exception as e:
            print("找不到images， " + e.__str__())

        try:
            description = chrome_driver_instance.find_element(By.XPATH, "//div[@class='Rte']").text
        except Exception as e:
            print("找不到description， " + e.__str__())

        _connection = getDatabaseConnection4Jubilee()

        _cursor = _connection.cursor()

        _cursor.execute("insert into jubilee_Product_scrapy(title, price, description, images, category) "
                        "values ('" + quote(title) + "', '" +
                        str(price) + "', '" + quote(description) + "', '" + image + "', '" + _category + "')")

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


def listProducts(_url, _userName, _category):
    global chrome_driver_instance

    try:
        createChromeDriver(_userName)

        total = JubileeConfig.jubileeConfig['jubilee']['totalPages']
        count = JubileeConfig.jubileeConfig['jubilee']['begin']
        urls = []
        while count <= total:
            actualUrl = _url + "?page=" + str(count)

            chrome_driver_instance.get(actualUrl)

            time.sleep(5)

            preLoading()

            details = chrome_driver_instance.find_elements(By.XPATH,
                                                           "//a[contains(@class, 'ProductItem__ImageWrapper')]")
            for detail in details:
                urls.append(detail.get_attribute('href'))

            count = count + 1

        for detailUrl in urls:
            detailProduct(detailUrl, _category)

    except Exception as e:
        print(e.__str__)
    finally:
        if chrome_driver_instance:
            chrome_driver_instance.close()


if __name__ == '__main__':
    listProducts(JubileeConfig.jubileeConfig['jubilee']['initUrl'],
                 JubileeConfig.jubileeConfig['jubilee']['userName'],
                 JubileeConfig.jubileeConfig['jubilee']['category'])
