import json
from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.service import Service
import threading
import aliWangWangConfig

global_chrome_driver_instances = []
global_chat_lock = threading.Lock()

message_count = 0


def createChromeInstance(userName):
    if not os.path.exists(
            aliWangWangConfig.aliWangWangConfig['aliWangWang']['cookieDir'] + userName + ".cookie"):
        return None

    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Version: 126, Browser and Driver
        if aliWangWangConfig.aliWangWangConfig['aliWangWang']['prod'] == 1:
            service = Service('/opt/ansible/ansible/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome()

        driver.get("https://www.1688.com")

        time.sleep(2)

        driver.delete_all_cookies()

        file = open(aliWangWangConfig.aliWangWangConfig['aliWangWang']['cookieDir'] + userName + ".cookie", 'r')
        cookie_str = file.read()
        file.close()
        cookies = json.loads(cookie_str)

        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()

        return driver
    except Exception as e:
        print(e.__str__())

        return None


def initChromePool():
    users = aliWangWangConfig.aliWangWangConfig['aliWangWang']['users']
    for user in users:
        connection = createChromeInstance(user)
        if connection is not None:
            global_chrome_driver_instances.append({'userName': user, 'driver': connection})
            print("链接创建成功，" + user)

    print("初始化链接池完成.")


def destroyPool():
    for conn in global_chrome_driver_instances:
        conn['driver'].close()
        print("销毁链接成功：" + conn['userName'])

    global_chrome_driver_instances.clear()

    print("销毁完所有的链接.")


def getChromeInstance(userName):
    for conn in global_chrome_driver_instances:
        if userName == conn['userName']:
            return conn['driver']

    return None


def getDriverInstance(userName):
    global message_count
    if message_count > aliWangWangConfig.aliWangWangConfig['aliWangWang']['count']:
        destroyPool()
        initChromePool()
        message_count = 0
    else:
        message_count = message_count + 1

    return getChromeInstance(userName)


initChromePool()
