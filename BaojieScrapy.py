import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class BaojieScrapy(CommonScrapy):

    def getProductListByCategories(self):
        return [
            'https://www.st-baojie.com/products'
        ]

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='products']"
                                    "//ul"
                                    "/li"
                                    "//div[@class='h4']"
                                    "/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return list(set(urls))

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'main_text')]"
                                       "//h1[@class='pro_main_title']").text
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@id='parentHorizontalTab01']"
                                       "//div[@class='tab_list']").text
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[@class='pro_page']"
                                        "//div[contains(@class, 'main')]"
                                        "/div[contains(@class, 'sp-wrap')]"
                                        "/div[contains(@class, 'sp-thumbs')]"
                                        "/a")
            for image in images:
                imageUrls.append(image.get_attribute('href'))

            image = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='pro_page']"
                                       "//div[contains(@class, 'main')]"
                                       "/div[contains(@class, 'sp-wrap')]"
                                       "/div[contains(@class, 'sp-large')]"
                                       "/a")

            imageUrls.append(image.get_attribute('href'))

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
        BaojieScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
