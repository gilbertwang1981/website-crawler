import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class AtcacarScrapy(CommonScrapy):
    def __init__(self, chromeDriver):
        self.chrome = chromeDriver

    def getProductListByCategories(self):
        categories = self.chrome.find_elements(By.XPATH, "//ul[@class='product-categories']/li/a")
        urls = []
        for category in categories:
            urls.append(category.get_attribute('href'))

        return urls

    def getProductDetailByList(self):
        details = self.chrome.find_elements(By.XPATH, "//div[contains(@class, 'porto-tb-item')]"
                                            "//div[contains(@class, 'product-list-content')]/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return urls

    def getProductDetail(self):
        return {
            'description': 'test description',
            'title': 'this is a product',
            'price': '10',
            'image': 'xxxx'
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        AtcacarScrapy(CommonScrapyProductService.getChromeDriver()),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
