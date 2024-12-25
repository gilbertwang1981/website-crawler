import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class CopexsolarScrapy(CommonScrapy):

    def getProductListByCategories(self):
        return ['http://www.copexsolar.com/our-products/']

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='product-thumbnail-outer-inner']"
                                    "/a[@class='woocommerce-LoopProduct-link']")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//h1[contains(@class, 'product_title')]").text
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@class='woocommerce-product-details__short-description']").text

            description = description + CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@id='tab-description']").text
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance.\
                find_elements(By.XPATH, "//div[@class='images']"
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
        CopexsolarScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
