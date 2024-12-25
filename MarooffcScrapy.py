import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class MarooffcScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categoryUrls = [
            'https://marooffc.com/shop/'
        ]

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@id='main-container']"
                                    "//ul[contains(@class, 'products')]"
                                    "/li[contains(@class, 'product')]"
                                    "/a[contains(@class, 'woocommerce-loop-product__link')]")

        detailsUrls = []
        for detail in details:
            detailsUrls.append(detail.get_attribute('href'))

        print(len(detailsUrls))

        return detailsUrls

    def getProductDetail(self):
        title = ''
        description = ''
        imageUrls = []

        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'summary')]"
                                       "//h1[contains(@class, 'product_title')]").text
        except Exception as e:
            e.__str__()

        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'summary')]"
                                       "//div[@class='woocommerce-product-details__short-description']").text

            description = description + CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'summary')]"
                                       "//div[@id='tab-description']").text

        except Exception as e:
            e.__str__()

        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[contains(@class, 'rtwpvg-thumbnail-image')]"
                                        "/img")

            for image in images:
                imageUrls.append(image.get_attribute('src'))
        except Exception as e:
            e.__str__()

        data = {
            'title': title,
            'description': description,
            'image': ','.join(imageUrls),
            'price': '',
            'sku': ''
        }

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        MarooffcScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
