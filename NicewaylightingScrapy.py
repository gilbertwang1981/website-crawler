import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class NicewaylightingScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categories = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='innersection']"
                                    "/div[@class='page-tit']"
                                    "/span"
                                    "/a")

        categoryUrls = []
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        print("类目数：" + str(len(categoryUrls)))

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//ul[contains(@class, 'wrap-products')]"
                                    "/li[@class='inner-one-pro']"
                                    "/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        print("商品数：" + str(len(urls)))

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='main-r']"
                                       "/div[@class='page-tit']"
                                       "/span").text
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance.\
                find_elements(By.XPATH, "//div[contains(@class, 'producut-view')]"
                                        "/div"
                                        "//img")
            for image in images:
                imageUrls.append(image.get_attribute('src'))

        except Exception as e:
            print(e.__str__())

        return {
            'description': '',
            'title': title,
            'price': '',
            'image': ','.join(imageUrls),
            'sku': ''
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        NicewaylightingScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
