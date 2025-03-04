import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import TiktokSamplingConfig
import json

chrome_driver_instance = None


def getCookie(_userName):
    cookie = open(TiktokSamplingConfig.tiktokSamplingConfig['tiktok']['cookieDirectory'] +
                  str(_userName) + ".cookie", 'r')
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


def createChromeDriver():
    global chrome_driver_instance

    if chrome_driver_instance:
        return

    try:
        s = Service(executable_path='/Users/gilbert/chromedriver-mac-x64/chromedriver')
        chrome_driver_instance = webdriver.Chrome(service=s)

        loadingC = TiktokSamplingConfig.tiktokSamplingConfig['tiktok']['loadingCookie']
        if loadingC == 1:
            chrome_driver_instance.get(TiktokSamplingConfig.tiktokSamplingConfig['tiktok']['loadingCookieUrl'])

            time.sleep(1)

            userName = TiktokSamplingConfig.tiktokSamplingConfig['tiktok']['userName']

            loadingCookie(userName)
    except Exception as e:
        print(e.__str__())


def scrollingPage():
    enable = TiktokSamplingConfig.tiktokSamplingConfig['tiktok']['scrolling']
    if enable == 0:
        return

    c = 0
    off = TiktokSamplingConfig.tiktokSamplingConfig['tiktok']['scrollingOffset']
    totalTimes = TiktokSamplingConfig.tiktokSamplingConfig['tiktok']['scrollingTimes']
    duration = TiktokSamplingConfig.tiktokSamplingConfig['tiktok']['scrollingDuration']
    while c < totalTimes:
        off = off + c * 100
        chrome_driver_instance.execute_script("window.scrollBy(0," + str(off) + ")")

        time.sleep(duration)

        c = c + 1


def closeChromeDriver():
    chrome_driver_instance.close()


def sampling():
    celebrities = ['https://www.tiktok.com/@yeahboxprox']

    for celebrity in celebrities:
        chrome_driver_instance.get(celebrity)

        time.sleep(1)

        scrollingPage()

        videos = chrome_driver_instance.find_elements(By.XPATH,
                                                      "//div[contains(@class, 'css-1uqux2o-DivItemContainerV2')]"
                                                      "//a")
        for video in videos:
            print(video.get_attribute('href'))


def initialize_scrapy():
    createChromeDriver()
    sampling()
    closeChromeDriver()


if __name__ == '__main__':
    initialize_scrapy()
