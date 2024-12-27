import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class MarjanalsahraScrapy(CommonScrapy):

    def __init__(self):
        self.titles = []
        self.imageUrls = []
        self.index = 0

    def getProductListByCategories(self):
        categoryUrls = []

        categories = CommonScrapyProductService.chrome_driver_instance.\
            find_elements(By.XPATH, "//li[@id='menu-item-61']"
                                    "//div[@class='mega-menu']"
                                    "//a")
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@id='vlightbox1']"
                                    "/a[@class='vlightbox1']")

        detailsUrls = []
        for detail in details:
            detailsUrls.append('https://www.marjanalsahra.com/')
            self.titles.append(detail.text)
            self.imageUrls.append(detail.get_attribute('href'))

        return detailsUrls

    def getProductDetail(self):
        data = {
            'title': self.titles[self.index],
            'description': '',
            'image': self.imageUrls[self.index],
            'price': '',
            'sku': ''
        }

        self.index = self.index + 1

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        MarjanalsahraScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
