import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class OveisgharanScrapy(CommonScrapy):

    def __init__(self):
        self.titles = []
        self.images = []
        self.index = 0

    def getProductListByCategories(self):
        categoryUrls = [
            'https://oveisgharan.ae/shop/'
        ]

        return categoryUrls

    def getProductDetailByList(self):

        titles = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[contains(@class, 'product-small')]"
                                    "//div[contains(@class,'box-text')]"
                                    "/div[@class='title-wrapper']"
                                    "/p[contains(@class, 'product-title')]"
                                    "/a")

        images = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[contains(@class, 'product-small')]"
                                    "//div[@class='box-image']"
                                    "/div"
                                    "/a/img")

        categoryUrls = []
        i = 0
        while i < len(titles):
            self.titles.append(titles[i].text)
            self.images.append(images[i].get_attribute('data-src'))

            categoryUrls.append(titles[i].get_attribute('href'))

            i = i + 1

        return categoryUrls

    def getProductDetail(self):
        data = {
            'description': '',
            'title': self.titles[self.index],
            'price': '',
            'image': self.images[self.index],
            'sku': ''
        }

        print(data)

        self.index = self.index + 1

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        OveisgharanScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
