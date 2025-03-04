import time

import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class Pamir121Scrapy(CommonScrapy):

    def __init__(self):
        self.imageUrls = []
        self.titles = []
        self.index = 0

    def getProductListByCategories(self):
        categoryUrls = []

        categories = CommonScrapyProductService.chrome_driver_instance.\
            find_elements(By.XPATH, "//li[@id='comp-l09fiwfn3']"
                                    "/ul"
                                    "//a")

        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        return categoryUrls

    def getProductDetailByList(self):
        images = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='pro-gallery-parent-container']"
                                    "//div[contains(@class, 'gallery-item-container')]"
                                    "//img")

        eTitles = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='pro-gallery-parent-container']"
                                    "//div[contains(@class, 'info-element-title')]"
                                    "/span")

        urls = []
        count = 0
        for image in images:
            self.imageUrls.append(image.get_attribute('src'))
            self.titles.append(eTitles[count].text)

            urls.append(CommonScrapyProductService.chrome_driver_instance.current_url)

            count = count + 1

        return urls

    def getProductDetail(self):
        data = {
            'description': '',
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
        Pamir121Scrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
