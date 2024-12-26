import time

import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

import PlatoledConfig

chrome_driver_instance = None


def getDatabaseConnection():
    mysqlConn = pymysql.connect(host=PlatoledConfig.platoledConfig['platoled']['db']['host'],
                                port=PlatoledConfig.platoledConfig['platoled']['db']['port'],
                                user=PlatoledConfig.platoledConfig['platoled']['db']['user'],
                                password=PlatoledConfig.platoledConfig['platoled']['db']['pass'],
                                database=PlatoledConfig.platoledConfig['platoled']['db']['dbName'])

    return mysqlConn


def createChromeDriver():
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        chrome_driver_instance = webdriver.Chrome()
    except Exception as e:
        print(e.__str__())


def insert(_title, _description, _image):
    try:
        _connection = getDatabaseConnection()

        _cursor = _connection.cursor()

        _cursor.execute("insert into common_product_scrapy(title, images, category, description) "
                        "values ('" + quote(_title) + "', '"
                        + _image + "', 'platoled', '" + quote(_description) + "')")

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


def handleProducts(_url):
    print("READY TO SCRAPY " + _url)

    chrome_driver_instance.get(_url)

    time.sleep(3)

    i = 0
    while i < 8:
        if i == 0:
            chrome_driver_instance.execute_script("window.scrollBy(0," + str(200) + ")")

            time.sleep(2)

        clickButtons = chrome_driver_instance.find_elements(By.XPATH, "//div[@id='product-container']"
                                                                      "/div[contains(@class, 'product-card')]"
                                                                      "/button")

        for button in clickButtons:
            button.click()

            time.sleep(2)

            title = ''
            description = ''
            imageUrl = ''

            try:
                description = chrome_driver_instance.find_element(By.XPATH, "//div[@class='modal-content']"
                                                                            "//div[contains(@class, 'modal-body')]"
                                                                            "/div[2]").text

                title = description.split('\n')[0][len("Product name "):]
            except Exception as e:
                print(e.__str__())

            try:
                imageUrl = chrome_driver_instance.find_element(By.XPATH, "//div[@class='modal-content']"
                                                                         "//div[contains(@class, 'modal-body')]"
                                                                         "/div"
                                                                         "/img").get_attribute('src')
            except Exception as e:
                print(e.__str__())

            try:
                chrome_driver_instance.find_element(By.XPATH, "//div[@class='modal-footer']"
                                                              "/button").click()
                time.sleep(2)
            except Exception as e:
                e.__str__()

            insert(title, description, imageUrl)

            if i == 7:
                chrome_driver_instance.execute_script("window.scrollBy(0," + str(200) + ")")

                time.sleep(2)

                try:
                    chrome_driver_instance.find_element(By.XPATH, "//div[@id='paginationContainer']"
                                                                  "/span[contains(@class, 'next-button')]").click()

                    i = 0

                    time.sleep(2)
                except Exception as e:
                    print(e.__str__())
                    return
            else:
                i = i + 1

        if len(clickButtons) < 8:
            return


def listProducts(_url):
    global chrome_driver_instance

    try:
        createChromeDriver()

        chrome_driver_instance.get(_url)

        time.sleep(1)

        categories = chrome_driver_instance.find_elements(By.XPATH, "//div[@id='navbarSupportedContent']"
                                                                    "//li[@class='nav-item ']"
                                                                    "//div[@class='dropdown-content']"
                                                                    "/a")
        categoryUrls = []
        for category in categories:
            cat = category.get_attribute('onclick')
            cat = cat[len("passName(") + 1:-2]
            categoryUrls.append("http://www.platoled.com/product.html?category=" + quote(cat))

        for url in categoryUrls:
            handleProducts(url)
    except Exception as e:
        e.__str__
    finally:
        if chrome_driver_instance:
            chrome_driver_instance.close()


if __name__ == '__main__':
    listProducts(PlatoledConfig.platoledConfig['platoled']['initUrl'])
