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
        title = ''
        try:
            title = self.chrome.find_element(By.XPATH, "//h2[contains(@class, 'product_title')]").text
        except Exception as e:
            e.__str__()

        description = ''
        try:
            description = self.chrome.find_element(By.XPATH, "//div[@id='tab-description']").text
        except Exception as e:
            e.__str__()

        imageUrls = []
        try:
            images = self.chrome.find_elements(By.XPATH, "//div[contains(@class, 'product-image-slider')]"
                                                         "//div[@class='img-thumbnail']"
                                                         "//img")
            for image in images:
                img = image.get_attribute('src')
                img = img[:img.find('?')]
                imageUrls.append(img)

        except Exception as e:
            e.__str__()

        return {
            'description': description,
            'title': title,
            'price': '',
            'image': ','.join(imageUrls)
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        AtcacarScrapy(CommonScrapyProductService.getChromeDriver()),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()