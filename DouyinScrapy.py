import concurrent
import time
from concurrent.futures import ThreadPoolExecutor

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

command_executor = "http://localhost:4723"

times = 50


def getUser():
    ele = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView'
                                                       '[@resource-id="com.ss.android.ugc.aweme:id/rwt"]')

    return ele.text


def getFans():
    ele = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView'
                                                       '[@resource-id="com.ss.android.ugc.aweme:id/351"]')
    return ele.text


def getLikes():
    ele = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView'
                                                       '[@resource-id="com.ss.android.ugc.aweme:id/35u"]')

    return ele.text


def getConcerns():
    ele = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView'
                                                       '[@resource-id="com.ss.android.ugc.aweme:id/35x"]')

    return ele.text


def getWorks():
    ele = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView'
                                                       '[@resource-id="android:id/text1"]')

    return ele.text.split(' ')[1]


if __name__ == '__main__':
    desired_caps = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='Android',
        appPackage='com.ss.android.ugc.aweme',
        appActivity='.main.MainActivity',
        noReset='true',
        fullReset='false',
        uiautomator2ServerInstallTimeout='10000',
        unicodeKeyboard='true',
        resetKeyboard='true'
    )
    options = UiAutomator2Options().load_capabilities(desired_caps)

    driver = webdriver.Remote(command_executor=command_executor, options=options)

    time.sleep(1)

    i = 0
    while i < times:
        try:
            driver.tap([(650, 500)])

            with ThreadPoolExecutor(max_workers=5) as executor:
                future1 = executor.submit(getUser)
                future2 = executor.submit(getFans)
                future3 = executor.submit(getLikes)
                future4 = executor.submit(getConcerns)
                future5 = executor.submit(getWorks)

            try:
                result1 = future1.result(timeout=10)
                result2 = future2.result(timeout=10)
                result3 = future3.result(timeout=10)
                result4 = future4.result(timeout=10)
                result5 = future5.result(timeout=10)
            except concurrent.futures.TimeoutError as err:
                err.__str__()
            finally:
                if result1 and result2:
                    print("用户：" + result1 + " 粉丝：" + result2 + " 点赞数：" +
                          result3 + " 关注数：" + result4 + " 作品数：" + result5)
        except Exception as e:
            e.__str__()
        finally:
            driver.back()

            time.sleep(1)

            driver.flick(450, 450, 490, 20)

            time.sleep(1)

            i = i + 1

    driver.quit()
