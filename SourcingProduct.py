import json
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import pyautogui


def publishSourcing(userName, subject, amount, price, desc,
                    categoryOne, categoryTwo, categoryThree,
                    addrOne, addrTwo, addrThree):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Version: 126, Browser and Driver
        service = Service('/opt/ansible/ansible/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get("https://www.1688.com")

        time.sleep(3)

        driver.delete_all_cookies()

        file = open("/opt/apps/kp-1688-sourcing/" + userName + ".cookie", 'r')
        # file = open(userName + ".cookie", 'r')

        cookie_str = file.read()
        file.close()
        cookies = json.loads(cookie_str)

        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()

        sourcingUrl = "https://pinpai.1688.com/page/p_mro_post_buyoffer.htm?" \
                      "source=open&entrySource=work&entrySource=work"

        driver.get(sourcingUrl)

        time.sleep(5)

        driver.maximize_window()

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='subject']").send_keys(subject)

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='customCategory']").click()

        time.sleep(1)

        offset = 0
        while offset < categoryOne:
            pyautogui.press('down')
            offset += 1

        if categoryOne != -1:
            pyautogui.press('enter')

        offset = 0
        while offset < categoryTwo:
            pyautogui.press('down')
            offset += 1

        if categoryTwo != -1:
            pyautogui.press('enter')

        offset = 0
        while offset < categoryThree:
            pyautogui.press('down')
            offset += 1

        if categoryThree != -1:
            pyautogui.press('enter')

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='amount']").send_keys(amount)

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='price']").send_keys(price)

        time.sleep(1)

        driver.find_element(By.XPATH, "//textarea[@id='description']").send_keys(desc)

        time.sleep(1)

        driver.find_element(By.XPATH, "//div[@class='upload--dft']/img").click()

        time.sleep(1)

        pyautogui.typewrite(r'/tmp/test.png', interval=0.1)

        time.sleep(1)

        pyautogui.press('enter')

        time.sleep(1)

        pyautogui.press('enter')

        time.sleep(1)

        el = driver.find_element(By.XPATH, "//input[@class='next-checkbox-input']")
        el.click()
        time.sleep(1)
        el.click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//span[text()='下一步']").click()

        time.sleep(2)

        driver.find_element(By.XPATH, "//input[@id='receiveAddressCode']").click()

        time.sleep(1)

        offset = 0
        while offset < addrOne:
            pyautogui.press('down')
            offset += 1

        if addrOne != -1:
            pyautogui.press('enter')

        offset = 0
        while offset < addrTwo:
            pyautogui.press('down')
            offset += 1

        if addrTwo != -1:
            pyautogui.press('enter')

        offset = 0
        while offset < addrThree:
            pyautogui.press('down')
            offset += 1

        if addrThree != -1:
            pyautogui.press('enter')

        time.sleep(1)

        dt = driver.find_element(By.XPATH, "//input[@placeholder='请选择日期']")
        dt.click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@class='next-calendar-btn']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[text()='7月']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[text()='12']").click()
        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='sendWay']").click()
        time.sleep(1)

        el30 = driver.find_element(By.XPATH, "//span[text()='物流站点自提']")
        el30.click()
        el30.click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//input[@id='invoiceType']").click()
        time.sleep(1)

        el40 = driver.find_element(By.XPATH, "//span[text()='不用发票']")
        el40.click()
        el40.click()

        time.sleep(1)

        driver.find_element(By.XPATH, "//textarea[@id='remark']").send_keys("无备注")

        time.sleep(1)

        inputs = driver.find_elements(By.XPATH, "//input[@placeholder='请选择日期']")
        inputs[1].click()

        driver.find_element(By.XPATH, "//button[contains(text(), '月')]").click()
        time.sleep(1)

        driver.find_element(By.XPATH, "//div[text()='7月']").click()
        time.sleep(1)

        days = driver.find_elements(By.XPATH, "//div[text()='2']")
        days[1].click()
        time.sleep(1)

        driver.find_element(By.XPATH, "//button[@groupid='submit']/span[text()='立即发布']").click()

        time.sleep(1)
    finally:
        driver.close()
