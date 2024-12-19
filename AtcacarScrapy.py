import time

import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class AtcacarScrapy(CommonScrapy):

    def __init__(self):
        self.titles = []
        self.index = 0

    def getProductListByCategories(self):
        urls = [
            'https://shop.atcacar.com/product-category/automotive-accessories/'
            'https://shop.atcacar.com/product-category/camping-outdoor-and-tools/',
            'https://shop.atcacar.com/product-category/consumer-electronics-accessories/'
        ]

        return urls

    def getProductDetailByList(self):
        time.sleep(5)

        self.titles = []
        self.index = 0

        details = CommonScrapyProductService. \
            chrome_driver_instance.find_elements(By.XPATH, "//div[contains(@class, 'product-list-content')]"
                                                           "/h3"
                                                           "/a")

        urls = []
        i = 0
        for detail in details:
            urls.append(detail.get_attribute('href'))

            if detail.text:
                i = i + 1
                self.titles.append(detail.text)

        return urls

    def getProductDetail(self):
        imageUrls = []
        try:
            images = CommonScrapyProductService. \
                chrome_driver_instance.find_elements(By.XPATH, "//div[contains(@class, 'product-thumbnails')]"
                                                               "//div[@class='img-thumbnail']"
                                                               "/img")
            for image in images:
                imageUrls.append(image.get_attribute('src').split("?")[0])
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH,
                             "//div[@id='tab-description']").text
        except Exception as e:
            print(e.__str__())

        data = {
            'description': description,
            'title': self.titles[self.index],
            'price': '',
            'image': ','.join(imageUrls),
            'sku': ''
        }

        self.index = self.index + 1

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        AtcacarScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
