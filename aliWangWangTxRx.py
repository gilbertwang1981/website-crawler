import json
import time

import requests

import aliWangWangConfig
from aliWangWangChat import ChatObject
import aliWangWangConnection
from selenium.webdriver.common.by import By
from ProductDetail import Product


def reloadChromePool():
    with aliWangWangConnection.global_chat_lock:
        aliWangWangConnection.destroyPool()
        aliWangWangConnection.initChromePool()


def getProductDetail(offerId, userName):
    with aliWangWangConnection.global_chat_lock:
        try:
            driver = aliWangWangConnection.getDriverInstance(userName)
            if driver is None:
                return []

            detailUrl = 'https://detail.1688.com/offer/' + offerId + \
                        '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                        '&cosite=-&tracelog=p4p&_p_isad=1&' \
                        'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                        'sessionid=a659238081d473668bf0881d132d92ee'

            driver.get(detailUrl)

            time.sleep(1)

            title = driver.find_element(By.XPATH, "//div[contains(@class, 'title-text')]").text

            price = driver.find_elements(By.XPATH, "//span[contains(@class, 'price-text')]")

            start = driver.find_element(By.XPATH, "//span[contains(@class, 'unit-text')]").text

            products = driver.find_elements(By.XPATH, "//div[@class='od-pc-attribute']//div[@class='offer-attr-list']"
                                                      "//div[@class='offer-attr-item']")

            crosses = driver.find_elements(By.XPATH, "//div[@class='od-pc-offer-cross']//div[@class='offer-attr-list']"
                                                     "//div[@class='offer-attr-item']")

            p = Product()

            propsImages = driver.find_elements(By.XPATH, "//div[@class='prop-img']")
            propsNames = driver.find_elements(By.XPATH, "//div[@class='prop-name']")

            index = 0
            for name in propsNames:
                colorUrl = ''
                if (len(propsImages) - 1) >= index:
                    colorUrl = propsImages[index].get_attribute("style")
                    begin = colorUrl.find("url(\"") + 5
                    end = colorUrl.find("\")")

                    colorUrl = colorUrl[begin: end]

                colorTitle = name.text
                color = {
                    "url": colorUrl,
                    "title": colorTitle
                }

                p.colors.append(color)

                index = index + 1

            try:
                driver.execute_script("window.scrollBy(0," + str(800) + ")")

                expand = driver.find_element(By.XPATH, "//div[@class='sku-wrapper-expend-button']")
                if expand.is_displayed():
                    expand.click()

                time.sleep(0.5)
            except Exception as e:
                print(e.__str__())
                pass

            skuNames = driver.find_elements(By.XPATH, "//div[@class='sku-item-name']")
            skuPrices = driver.find_elements(By.XPATH, "//div[@class='discountPrice-price']")
            skuStocks = driver.find_elements(By.XPATH, "//div[@class='sku-item-sale-num']")
            index = 0
            for name in skuNames:
                skuStock = '0'
                if skuStocks is not None and (len(skuStocks) - 1) >= index:
                    skuStock = skuStocks[index].text

                skuPrice = '0'
                if skuPrices is not None and (len(skuPrices) - 1) >= index:
                    skuPrice = skuPrices[index].text

                sku = {
                    "name": name.text,
                    "price": skuPrice,
                    "stock": skuStock
                }

                p.skus.append(sku)

                index = index + 1

            try:
                driver.execute_script("window.scrollBy(0," + str(1000) + ")")
                driver.find_element(By.XPATH, "//div[@class='offer-attr-switch']/i").click()
                time.sleep(0.5)
            except Exception as e:
                print(e.__str__())
                pass

            for product in products:
                pn = product.find_element(By.XPATH, "span[@class='offer-attr-item-name']").text
                pv = product.find_element(By.XPATH, "span[@class='offer-attr-item-value']").text
                if len(pn) > 0 and len(pv) > 0:
                    p.pAttrs[pn] = pv

            for c in crosses:
                cn = c.find_element(By.XPATH, "span[@class='offer-attr-item-name']").text
                cv = c.find_element(By.XPATH, "span[@class='offer-attr-item-value']").text
                if len(cn) > 0 and len(cv) > 0:
                    p.pCross[cn] = cv

            p.price = price[0].text
            p.start = start

            c = 0
            off = 1000
            while c < 3:
                off = off + c * 3000
                driver.execute_script("window.scrollBy(0," + str(off) + ")")

                time.sleep(0.5)

                c = c + 1

            images = driver.find_elements(By.XPATH, "//img[@class = 'detail-gallery-img']")
            for image in images:
                p.images.append(image.get_attribute('src'))

            images = driver.find_elements(By.XPATH, "//img[@class = 'desc-img-loaded']")
            for image in images:
                p.images.append(image.get_attribute('src'))

            p.title = title

            try:
                driver.find_element(By.XPATH, "//span[contains(text(), '视频展示')]").click()

                time.sleep(0.5)

                p.video = driver.find_element(By.XPATH,
                                              "//div[@class='detail-video-wrapper']/video").get_attribute('src')
            except Exception as e:
                e.__str__()
                pass

            return p
        except Exception as e:
            print(e.__str__())

            return None


def getChatHistory(offerId, userName):
    with aliWangWangConnection.global_chat_lock:
        try:
            driver = aliWangWangConnection.getDriverInstance(userName)
            if driver is None:
                return []

            detailUrl = 'https://detail.1688.com/offer/' + offerId +\
                        '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                        '&cosite=-&tracelog=p4p&_p_isad=1&' \
                        'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                        'sessionid=a659238081d473668bf0881d132d92ee'

            driver.get(detailUrl)

            time.sleep(1)

            driver.find_element(By.XPATH,
                                "//div[@class='pi-layout-container']"
                                "//a/img[contains(@src, '-tps-28') or contains(@src, '-tps-134')]").click()

            time.sleep(1)

            try:
                driver.find_element(By.XPATH, "//button[text()='优先使用网页版']").click()

                time.sleep(1)
            except Exception as e:
                e.__str__()

            windows = driver.window_handles
            driver.switch_to.window(windows[-1])

            chat_url = driver.find_element(By.XPATH, "//div[@id='ice-container']//iframe").get_attribute("src")

            driver.get(chat_url)

            time.sleep(1)

            elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-item-line')]")

            chatHistory = []

            for el in elements:
                content = el.text.split('\n')
                data = ChatObject()
                if len(content) >= 2:
                    data.user = content[0]
                    data.time = content[1]
                    if len(content) > 2:
                        data.chats.append(content[2])

                    chatHistory.append(data)

            return chatHistory
        except Exception as e:
            e.__str__()

            return []


def chatWithCustomer(offerId, chatList, userName):
    with aliWangWangConnection.global_chat_lock:
        try:
            driver = aliWangWangConnection.getDriverInstance(userName)
            if driver is None:
                return

            detailUrl = 'https://detail.1688.com/offer/' + offerId + \
                        '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                        '&cosite=-&tracelog=p4p&_p_isad=1&' \
                        'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                        'sessionid=a659238081d473668bf0881d132d92ee'

            driver.get(detailUrl)

            time.sleep(1)

            driver.find_element(By.XPATH,
                                "//div[@class='pi-layout-container']"
                                "//a/img[contains(@src, '-tps-28') or contains(@src, '-tps-134')]").click()

            time.sleep(1)

            try:
                driver.find_element(By.XPATH, "//button[text()='优先使用网页版']").click()

                time.sleep(1)
            except Exception as e:
                e.__str__()

            windows = driver.window_handles
            driver.switch_to.window(windows[-1])

            chat_url = driver.find_element(By.XPATH, "//div[@id='ice-container']//iframe").get_attribute("src")

            driver.get(chat_url)

            time.sleep(2)

            for chatContent in chatList:
                driver.find_element(By.XPATH, "//div[@class='ww_input']//pre").send_keys(chatContent)

                driver.find_element(By.XPATH, "//div/button/span").click()

                time.sleep(1)

                productUrl = "https://detail.1688.com/offer/{}.html".format(offerId)
                content = "【消息发送日志】\n发送者：{} \n商品链接：{} \n内容：{}".format(userName, productUrl, chatContent)
                notifyWechat(content)
        except Exception as e:
            print(e.__str__())


def notifyWechat(content):
    headers = {
        'Content-Type': 'application/json'
    }

    message_data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }

    requests.post(aliWangWangConfig.aliWangWangConfig['aliWangWang']['wechatHook'],
                  data=json.dumps(message_data), headers=headers, verify=False)



