import time

import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class SkybeautyScrapy(CommonScrapy):

    def getProductListByCategories(self):
        time.sleep(10)
        categories = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//ul[contains(@class, 'wd-nav-product-cat')]"
                                    "//li[contains(@class, 'cat-item')]"
                                    "/a[@class='category-nav-link']")

        categoryUrls = []
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[contains(@class, 'product-grid-item')]"
                                    "/div[@class='product-wrapper']"
                                    "/div[contains(@class, 'product-element-bottom')]"
                                    "/h3[@class='wd-entities-title']"
                                    "/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return list(set(urls))

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'summary-inner')]"
                                       "//h1[contains(@class, 'product_title')]").text
            if "Product" in title:
                return {'description': '',
                        'title': '',
                        'price': '',
                        'image': '',
                        'sku': ''}
        except Exception as e:
            print(e.__str__())

        price = ''
        try:
            price = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'summary-inner')]"
                                       "//p[@class='price']"
                                       "//span[contains(@class, 'woocommerce-Price-amount')]").text
        except Exception as e:
            e.__str__()

        imageUrls = []
        try:
            image = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='product-image-wrap']"
                                       "//a")
            imageUrls.append(image.get_attribute('href'))

        except Exception as e:
            print(e.__str__())

        data = {
            'description': '',
            'title': title,
            'price': price,
            'image': ','.join(imageUrls),
            'sku': ''
        }

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        SkybeautyScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
