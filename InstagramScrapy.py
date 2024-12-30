import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_driver_instance = None


def getCookie(_userName):
    cookie = open('/Users/gilbert/instagram/' + str(_userName) + ".cookie", 'r')
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
        chrome_driver_instance = webdriver.Chrome()

        chrome_driver_instance.get('https://www.instagram.com/')

        time.sleep(1)

        loadingCookie('qingfeng')

    except Exception as e:
        e.__str__()
        if chrome_driver_instance:
            chrome_driver_instance.close()


def scrollingPage():
    c = 0
    off = 2500
    totalTimes = 10
    duration = 1
    while c < totalTimes:
        off = off + c * 3000
        chrome_driver_instance.execute_script("window.scrollBy(0," + str(off) + ")")

        time.sleep(duration)

        c = c + 1


def scrapyFans(userName):
    try:
        chrome_driver_instance.get('https://www.instagram.com/' + userName)

        time.sleep(1)

        number = chrome_driver_instance.find_element(By.XPATH, "//div[contains(text(), '帖子')]")
        print("帖子数：" + number.text)

        try:
            fanNumber = chrome_driver_instance.find_element(By.XPATH, "//a[contains(text(), '粉丝')]")
            print("粉丝数：" + fanNumber.text)
        except Exception as e:
            e.__str__()

            fanNumber = chrome_driver_instance.find_element(By.XPATH, "//button[contains(text(), '粉丝')]")
            print("粉丝数：" + fanNumber.text)

        try:
            chrome_driver_instance.find_element(By.XPATH, "//a[text()='关注']").click()
        except Exception as e:
            e.__str__()
            chrome_driver_instance.find_element(By.XPATH, "//button[text()='关注']").click()

        time.sleep(3)

        scrollingPage()

        time.sleep(5)

        fansUrls = chrome_driver_instance.find_elements(By.XPATH, "//div[@class='x1rg5ohu']"
                                                                 "/div"
                                                                 "/a")

        fanNames = chrome_driver_instance.find_elements(By.XPATH, "//div[@class='x1rg5ohu']"
                                                                  "/div"
                                                                  "/a"
                                                                  "//span")

        index = 0
        fanUrls = []
        for fanUrl in fansUrls:
            if '推荐' in fanNames[index].text:
                break
            else:
                url = fanUrl.get_attribute('href')
                index = index + 1

                fanUrls.append(url)
        print("关注：" + fanUrls.__str__())
    except Exception as e:
        print(e.__str__())


if __name__ == '__main__':
    createChromeDriver()

    users = [
        'momobethe1',
        'kenny__mendez',
        'justangeline',
        'stevomd123',
        'presterjere'
    ]

    print('爬取instagram用户数据,' + users.__str__())

    for user in users:
        print("用户：" + user)

        scrapyFans(user)

        print("\n\n")

    if chrome_driver_instance:
        chrome_driver_instance.close()
