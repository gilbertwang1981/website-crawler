import json
from selenium import webdriver
import time
import threading
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import aliImageSearchConfig
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os

thread_pool_lock = threading.Lock()

chrome_drivers = []


def getCookie(userName):
    filePath = aliImageSearchConfig.aliImageSearchConfig['aliImageSearch']['cookieDir'] + userName + ".cookie"
    if not os.path.exists(filePath):
        return []

    file = open(filePath, 'r')
    cookie_str = file.read()
    file.close()
    cookies = json.loads(cookie_str)

    return cookies


def initChrome(userName):
    try:
        # Version: 126, Browser and Driver
        if aliImageSearchConfig.aliImageSearchConfig['aliImageSearch']['prod'] == 1:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--single-process')
            chrome_options.add_argument('--disable-dev-shm-usage')

            service = Service('/opt/ansible/ansible/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome()

        driver.get("https://www.1688.com")

        time.sleep(1)

        driver.delete_all_cookies()

        cookies = getCookie(userName)
        if len(cookies) == 0:
            driver.close()

            return None

        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()

        driver.get("https://s.1688.com/selloffer/offer_search.html")

        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'alisearch-input')))

        return driver
    except Exception as e:
        print(e.__str__())

        return None


def createDriver(userName):
    return initChrome(userName)


def createChromePool():
    global chrome_drivers
    for user in aliImageSearchConfig.aliImageSearchConfig['aliImageSearch']['users']:
        _driver = createDriver(user)
        if _driver is not None:
            print("创建链接成功，" + user)
            chrome_drivers.append({'driver': _driver, 'userName': user})

    print("链接池初始化完成")


def getDriverFromPool(userName):
    for conn in chrome_drivers:
        if conn['userName'] == userName:
            return conn['driver']

    return None


def destroyPool():
    global chrome_drivers
    for conn in chrome_drivers:
        conn['driver'].close()
        print("销毁链接成功：" + conn['userName'])

    chrome_drivers.clear()

    print("销毁完所有的链接.")


def reloadChromePool():
    destroyPool()
    createChromePool()


def aliSearch(imageUrl, userName):
    with thread_pool_lock:
        _driver = getDriverFromPool(userName)
        if _driver is None:
            return []

        try:
            element = _driver.find_element(By.XPATH, "//input[@id='alisearch-input']")
            element.send_keys(imageUrl)
            element.send_keys(Keys.RETURN)

            time.sleep(1)

            products = _driver.find_elements(By.XPATH, "//div[@class='img-container']/div/a/div[@class='img']")

            urls = []
            for detail in products:
                if len(urls) >= 5:
                    break

                urlStr = detail.get_attribute('style')

                begin = urlStr.index("url") + 5
                urlStr = urlStr[begin:len(urlStr) - 3]

                urls.append(urlStr)

            return urls
        except Exception as e:
            print(e.__str__())

            return []


def updateCookie(userName, cookie):
    with thread_pool_lock:
        cookiePath = aliImageSearchConfig.aliImageSearchConfig['aliImageSearch']['cookieDir']
        cookieFile = cookiePath + userName + '.cookie'

        if os.path.exists(cookieFile):
            os.remove(cookieFile)

        with open(cookieFile, 'w') as file:
            file.write(json.dumps(cookie))

        reloadChromePool()


createChromePool()
