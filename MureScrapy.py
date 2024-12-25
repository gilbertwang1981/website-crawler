import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class MureScrapy(CommonScrapy):

    def getProductListByCategories(self):
        return ['https://murexgeneraltrading.com/stationery-catalog/']

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='dt-css-grid']"
                                    "//h4[@class='entry-title']"
                                    "/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'page-title-head')]"
                                       "/h2[@class='entry-title']").text
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@id='tab-description']").text
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance.\
                find_elements(By.XPATH, "//div[contains(@class, 'woocommerce-product-gallery')]"
                                        "//ol[contains(@class, 'flex-control-thumbs')]"
                                        "/li"
                                        "/img")
            for image in images:
                imageUrls.append(image.get_attribute('src'))

        except Exception as e:
            print(e.__str__())

        return {
            'description': description,
            'title': title,
            'price': '',
            'image': ','.join(imageUrls),
            'sku': ''
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        MureScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
