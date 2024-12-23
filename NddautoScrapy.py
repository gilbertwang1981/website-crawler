import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class NddautoScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categoryUrls = [
            'https://nddauto.com/shop/'
        ]

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance.\
            find_elements(By.XPATH, "//div[contains(@class, 'wd-product')]"
                                    "/div[@class='product-wrapper']"
                                    "/div[contains(@class, 'product-element-top')]"
                                    "/a")

        detailsUrls = []
        for detail in details:
            detailsUrls.append(detail.get_attribute('href'))

        return detailsUrls

    def getProductDetail(self):

        title = ''
        price = ''
        description = ''
        imageUrl = ''

        try:
            title = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@class='product-image-summary']"
                                       "//div[contains(@class, 'summary')]"
                                       "//h1[contains(@class, 'product_title')]").text
        except Exception as e:
            e.__str__()

        try:
            price = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@class='product-image-summary']"
                                       "//div[contains(@class, 'summary')]"
                                       "//p[@class='price']"
                                       "//span[contains(@class, 'woocommerce-Price-amount')]").text
        except Exception as e:
            e.__str__()

        try:
            description = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@class='product-image-summary']"
                                       "//div[contains(@class, 'summary')]"
                                       "//div[@class='woocommerce-product-details__short-description']").text
        except Exception as e:
            e.__str__()

        try:
            image = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[contains(@class, 'product-images')]"
                                       "//div[@class='wd-carousel-wrap']"
                                       "//a")

            imageUrl = image.get_attribute('href')
        except Exception as e:
            e.__str__()

        data = {
            'description': description,
            'title': title,
            'price': price,
            'image': imageUrl,
            'sku': ''
        }

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        NddautoScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
