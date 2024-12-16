import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


# 有风控。基本上遍历7页就会被封，需要重新启动程序断点续传；
class RoyalfordScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categories = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//li[contains(@class, 'level-0')]/a")

        categoryUrls = []
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        # return categoryUrls[0]

        return ['https://royalford.ae/product-category/table-ware/']

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='product-content']//a[@class='product-image']")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH,
                             "//h2[contains(@class, "
                             "'product_title')]").text
        except Exception as e:
            e.__str__()

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='woocommerce-product-details__short-description']").text
        except Exception as e:
            e.__str__()

        sku = ''
        try:
            sku = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='woolentor_product_sku_info']/span[@class='sku']").text
        except Exception as e:
            e.__str__()

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[@class='flex-viewport']"
                                        "//div[@data-thumb]"
                                        "/a")

            if images:
                for image in images:
                    imageUrls.append(image.get_attribute('href'))
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
            'price': '',
            'image': ','.join(imageUrls),
            'sku': sku
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        RoyalfordScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
