import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class StargoldworldScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categoryUrls = [
            'https://stargoldworld.com/shop/'
        ]

        return categoryUrls

    def getProductDetailByList(self):

        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//h3[contains(@class,'woocommerce-loop-product__title')]"
                                    "/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH,
                             "//div[@class='product-title-wrap']"
                             "//h1[contains(@class, 'product_title')]").text
        except Exception as e:
            e.__str__()

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@id='tab-content-description']").text
        except Exception as e:
            e.__str__()

        price = ''
        try:
            price = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'summary')]"
                                       "//div[@class='entry-price-wrap']"
                                       "//div[@class='price']"
                                       "//span[contains(@class,'woocommerce-Price-amount')]").text
            price = price[3:]
        except Exception as e:
            e.__str__()

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[@class='woocommerce-product-gallery__image']"
                                        "//img")

            for image in images:
                imageUrls.append(image.get_attribute('src'))

        except Exception as e:
            e.__str__()

        return {
            'description': description,
            'title': title,
            'price': price,
            'image': ','.join(imageUrls),
            'sku': ''
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        StargoldworldScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
