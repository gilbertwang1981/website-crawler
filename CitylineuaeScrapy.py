import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class CitylineuaeScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categories = CommonScrapyProductService.chrome_driver_instance.\
            find_elements(By.XPATH, "//li[contains(@class, 'product-category')]"
                                    "/a")

        categoryUrls = []
        for category in categories:
            categoryUrl = category.get_attribute('href')
            categoryUrls.append(categoryUrl)

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='product-details-container']"
                                    "/h3[@class='product-title']"
                                    "/a")
        urls = []
        for detail in details:
            detailUrl = detail.get_attribute('href')
            urls.append(detailUrl)

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH,
                             "//h2[contains(@class, 'product_title')]").text
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@class='woocommerce-container']"
                                       "/div[@id='content']"
                                       "//div[contains(@class, 'woocommerce-tabs')]"
                                       "//div[@class='post-content']").text
        except Exception as e:
            e.__str__()

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance.\
                find_elements(By.XPATH, "//div[@class='images']"
                                        "/div[@id='slider']"
                                        "//ul[@class='slides']"
                                        "/li"
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
        CitylineuaeScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
