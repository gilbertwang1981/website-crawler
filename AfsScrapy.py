import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class AfsScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categories = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//ul[@id='menu-1-f4f1773']/li/a")

        categoryUrls = []
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//li[@id='productCard']/div/a")

        detailUrls = []
        for detail in details:
            detailUrls.append(detail.get_attribute('href'))
        return list(set(detailUrls))

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
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH,
                             "//div[@class='woocommerce-product-details__short-description']/ul").text
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH,
                              "//div[contains(@class, 'woocommerce-product-gallery--with-images')]"
                              "//div[@class='woocommerce-product-gallery__wrapper']"
                              "/div/a")
            for im in images:
                imageUrls.append(im.get_attribute('href'))

        except Exception as e:
            print(e.__str__())

        return {
            'description': description,
            'title': title,
            'price': '',
            'image': ','.join(imageUrls)
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        AfsScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
