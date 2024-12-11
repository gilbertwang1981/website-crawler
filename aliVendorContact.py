import time
from selenium import webdriver
import json
from selenium.webdriver.common.by import By

import aliVendorConfig
import pymysql


chrome_driver_instance = None


def getDatabaseConnection4Vendor():
    mysqlConn4Vendor = pymysql.connect(host=aliVendorConfig.aliVendorConfig['aliVendor']['db']['host'],
                                       port=aliVendorConfig.aliVendorConfig['aliVendor']['db']['port'],
                                       user=aliVendorConfig.aliVendorConfig['aliVendor']['db']['user'],
                                       password=aliVendorConfig.aliVendorConfig['aliVendor']['db']['pass'],
                                       database=aliVendorConfig.aliVendorConfig['aliVendor']['db']['dbName'])

    return mysqlConn4Vendor


def getCookie(_userName):
    cookie = open(aliVendorConfig.aliVendorConfig['aliVendor']['ali']['cookieDir'] + str(_userName) + ".cookie", 'r')
    cookie_str = cookie.read()
    cookie.close()

    return cookie_str


def getProductIds(_begin, _offset, _categoryOne, _categoryThree):
    try:
        _connection = getDatabaseConnection4Vendor()

        _cursor = _connection.cursor()
        _cursor.execute("select offer_id from product_vendor_1688 where category_one = '" +
                        _categoryOne + "' and category_three= '" + _categoryThree + "'order by id asc limit "
                        + str(_begin) + "," + str(_offset))
        _productIds = _cursor.fetchall()

        _connection.commit()

        return _productIds
    except Exception as e:
        print(e.__str__())
        if _connection:
            _connection.rollback()

        return []
    finally:
        if _cursor:
            _cursor.close()
        if _connection:
            _connection.close()


def createChromeDriver(cookieName):
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        chrome_driver_instance = webdriver.Chrome()

        chrome_driver_instance.get("https://www.1688.com")

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


def initProductIds(_userName, _categoryUrl, _categoryOne, _categoryThree):
    global chrome_driver_instance
    try:
        createChromeDriver(_userName)

        chrome_driver_instance.get(_categoryUrl)

        time.sleep(1)

        c = 0
        off = 2000
        while c < 15:
            off = off + c * 3000
            chrome_driver_instance.execute_script("window.scrollBy(0," + str(off) + ")")

            time.sleep(1)

            c = c + 1

        offerIds = chrome_driver_instance.find_elements(By.XPATH, "//div[@class='list']/div")

        i = 0
        _connection = getDatabaseConnection4Vendor()
        _cursor = _connection.cursor()
        while i < len(offerIds):
            if offerIds[i].get_attribute('id') != '':
                _offerId = offerIds[i].get_attribute('id')
                try:
                    _cursor.execute("insert into product_vendor_1688(offer_id, category_one, category_three) "
                                    "values('" + _offerId + "', '" + _categoryOne + "', '" + _categoryThree + "')")
                except Exception as e:
                    print(e.__str__())
                    _connection.rollback()
                else:
                    _connection.commit()
            i = i + 1

        print("初始化数据集." + str(len(offerIds)))

    except Exception as e:
        print(e.__str__())
    finally:
        if _cursor:
            _cursor.close()
        if _connection:
            _connection.close()


def scrapVendorsByCategory(_categoryUrl, _userName, _productIds):
    global chrome_driver_instance
    try:
        createChromeDriver(_userName)

        print("本次要处理的商品数:" + str(len(productIds)))

        i = 0
        _connection = getDatabaseConnection4Vendor()
        _cursor = _connection.cursor()
        while i < len(productIds):
            detailUrl = 'https://detail.1688.com/offer/' + productIds[i] + \
                        '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                        '&cosite=-&tracelog=p4p&_p_isad=1&' \
                        'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                        'sessionid=a659238081d473668bf0881d132d92ee'

            chrome_driver_instance.get(detailUrl)

            time.sleep(1)

            try:
                title = chrome_driver_instance.find_element(By.XPATH, "//div[@class='title-text']").text

                chrome_driver_instance.find_element(By.XPATH, "//a[text()='联系方式']").click()

                time.sleep(1)

                windows = chrome_driver_instance.window_handles
                chrome_driver_instance.switch_to.window(windows[-1])
                chrome_driver_instance.maximize_window()

                phone = chrome_driver_instance.find_element(By.XPATH,
                                            "//div[contains(text(), '手机：')]/following-sibling::*[position()=1]").text

                company = chrome_driver_instance.find_element(By.XPATH,
                                              "//div[text()='联系方式']/following-sibling::*[position()=1]").text
            except Exception as e:
                i = i + 1
                e.__str__()
                continue

            try:
                if phone != '' and not phone.__contains__('暂无'):
                    _cursor.execute("update product_vendor_1688 set title='" + title + "', mobile=" + str(phone) +
                                    ", company='" + company + "' where offer_id=" + str(productIds[i]))
            except Exception as e:
                e.__str__()
                _connection.rollback()
            else:
                _connection.commit()

            i = i + 1

            windows = chrome_driver_instance.window_handles
            chrome_driver_instance.switch_to.window(windows[-1])
    except Exception as e:
        print(e.__str__())
        if _connection:
            _connection.rollback()
    finally:
        if chrome_driver_instance:
            chrome_driver_instance.close()
        if _cursor:
            _cursor.close()
        if _connection:
            _connection.close()


if __name__ == '__main__':
    url = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['categoryUrl']
    userName = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['user']
    categoryOne = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['categoryOne']
    categoryThree = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['categoryThree']
    begin = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['begin']
    offset = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['offset']

    rows = getProductIds(begin, offset, categoryOne, categoryThree)
    if rows.__len__() <= 0:
        initProductIds(userName, url, categoryOne, categoryThree)

    rows = getProductIds(begin, offset, categoryOne, categoryThree)
    productIds = []
    for row in rows:
        productIds.append(row[0])

    scrapVendorsByCategory(url, userName, productIds)

