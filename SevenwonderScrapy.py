import time

import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class SevenwonderScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categories = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@id='navbarSupportedContent']"
                                    "/ul/li/ul/li/a")

        categoryUrls = []
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        return categoryUrls

    def getProductDetailByList(self):
        time.sleep(2)

        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[contains(@class, 'product-item')]"
                                    "/div[@class='product-thumb']"
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
                             "//div[contains(@class, 'pro-details-name')]"
                             "/h1").text
        except Exception as e:
            e.__str__()

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'product-detail-sort-des')]"
                                       "/h2").text
        except Exception as e:
            e.__str__()

        price = ''
        try:
            price = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'price-box')]"
                                       "/div/span").text
        except Exception as e:
            e.__str__()

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[contains(@class, 'pro-large-img')]"
                                        "/img")

            if images:
                for image in images:
                    imageUrls.append(image.get_attribute('src'))
            else:
                images = CommonScrapyProductService.chrome_driver_instance. \
                    find_element(By.XPATH, "//div[contains(@class, 'woocommerce-product-gallery')]"
                                           "//div[@data-thumb]"
                                           "/a")
                imageUrls.append(images.get_attribute('href'))

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
        SevenwonderScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
