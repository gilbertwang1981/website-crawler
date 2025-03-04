import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class GsbsolarScrapy(CommonScrapy):

    def getProductListByCategories(self):
        return [
            'https://gsbsolar.com/products/'
        ]

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='product-wrapper']"
                                    "//h3[@class='wd-entities-title']"
                                    "/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return list(set(urls))

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//h1[contains(@class, 'product_title')]").text
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@id='tab-description']"
                                       "/div").text
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            image = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'woocommerce-product-gallery')]"
                                       "//div[contains(@class, 'wd-gallery-images')]"
                                       "//div[@class='wd-carousel-wrap']"
                                       "//div[contains(@class, 'wd-carousel-item')]"
                                       "//img")
            imageUrls.append(image.get_attribute('src'))

            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[contains(@class, 'woocommerce-product-gallery')]"
                                        "/div[contains(@class, 'wd-gallery-thumb')]"
                                        "/div[@class='wd-carousel-inner']"
                                        "//div[contains(@class, 'wd-carousel-item')]"
                                        "/img")
            for image in images:
                imageUrls.append(image.get_attribute('src'))

        except Exception as e:
            print(e.__str__())

        data = {
            'title': title,
            'price': '',
            'image': ','.join(imageUrls),
            'sku': '',
            'description': description
        }

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        GsbsolarScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
