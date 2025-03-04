import time

import CommonScrapyConfig
import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class DiamondstarScrapy(CommonScrapy):
    def __init__(self):
        self.titles = []
        self.descriptions = []
        self.imageUrls = []
        self.index = 0

    def getProductListByCategories(self):
        categories = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//ul[@id='mobMenu']"
                                    "/li"
                                    "/a")

        categoryUrls = []
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        return list(set(categoryUrls))

    def getProductDetailByList(self):
        products = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//ul[@class='products']"
                                    "/li")

        urls = []
        for product in products:
            urls.append(CommonScrapyConfig.commonScrapyConfig['scrapy']['initUrl'])

            product.click()

            time.sleep(1)
            try:
                title = CommonScrapyProductService.chrome_driver_instance. \
                    find_element(By.XPATH, "//div[@id='example-popup']"
                                           "//div[contains(@class, 'images')]"
                                           "/img").get_attribute('title')
                self.titles.append(title)
            except Exception as e:
                print(e.__str__())
                self.titles.append('')

            try:
                description = CommonScrapyProductService.chrome_driver_instance. \
                    find_element(By.XPATH, "//div[@id='example-popup']"
                                           "//div[@class='woocommerce-tabs']"
                                           "//div[contains(@class, 'entry-content')]").text
                self.descriptions.append(description)
            except Exception as e:
                print(e.__str__())
                self.descriptions.append('')

            try:
                imageUrl = CommonScrapyProductService.chrome_driver_instance. \
                    find_element(By.XPATH, "//div[@id='example-popup']"
                                           "//div[contains(@class, 'images')]"
                                           "/img").get_attribute('src')
                self.imageUrls.append(imageUrl)
            except Exception as e:
                print(e.__str__())
                self.imageUrls.append('')

            CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@id='example-popup']"
                                       "//span[@class='popup-exit2']").click()

            time.sleep(1)

        return urls

    def getProductDetail(self):

        data = {
            'description': self.descriptions[self.index],
            'title': self.titles[self.index],
            'price': '',
            'image': self.imageUrls[self.index],
            'sku': ''
        }

        self.index = self.index + 1

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        DiamondstarScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
