import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class MaatScrapy(CommonScrapy):

    def getProductListByCategories(self):
        return ['https://maat.ae/shop/']

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//ul[contains(@class, 'products')]"
                                    "/li[contains(@class, 'ast-grid-common-col')]"
                                    "/div[@class='astra-shop-thumbnail-wrap']/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH,
                             "//h1[contains(@class, "
                             "'product_title')]").text
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
                find_elements(By.XPATH, "//div[@class='woocommerce-product-gallery__wrapper']"
                                        "/div"
                                        "/a")
            for image in images:
                imageUrls.append(image.get_attribute('href'))

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
        MaatScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
