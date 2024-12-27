import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class GhstorchlightScrapy(CommonScrapy):

    def __init__(self):
        self.titles = []
        self.imageUrls = []
        self.index = 0

    def getProductListByCategories(self):
        categories = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//li[@id='menu-item-301']"
                                    "//div[contains(@class, 'categories-style-default')]"
                                    "//div[@class='category-content']"
                                    "/a")

        categoryUrls = []
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='wpb_wrapper']"
                                    "//div[@class='basel-products-element']"
                                    "/div[contains(@class, 'products')]"
                                    "/div[contains(@class, 'product-grid-item')]"
                                    "/h3[@class='product-title']"
                                    "/a")

        images = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='wpb_wrapper']"
                                    "//div[@class='basel-products-element']"
                                    "/div[contains(@class, 'products')]"
                                    "/div[contains(@class, 'product-grid-item')]"
                                    "/div[@class='product-element-top']"
                                    "/a"
                                    "/img")
        i = 0
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))
            self.titles.append(detail.text)
            self.imageUrls.append(images[i].get_attribute('src'))

            i = i + 1

        return urls

    def getProductDetail(self):
        data = {
            'description': '',
            'title': self.titles[self.index],
            'price': '',
            'image': self.imageUrls[self.index],
            'sku': ''
        }

        print(data)

        self.index = self.index + 1

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        GhstorchlightScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
