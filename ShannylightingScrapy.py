import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class ShannylightingScrapy(CommonScrapy):

    def getProductListByCategories(self):
        return [
            'http://www.shannylighting.com/shanny/vip_doc/23417760_0_0_1.html'
        ]

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance.\
            find_elements(By.XPATH, "//h3[@class='pic-title']"
                                    "/a")

        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='pro-title']"
                                       "/h1[@class='h1-title']").text
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@id='proShowDetail_3']"
                                       "//div[@class='wap-add-img']").text
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance.\
                find_elements(By.XPATH, "//div[@id='proShowDetail_3']"
                                        "//div[@class='wap-add-img']"
                                        "/p"
                                        "/img")
            for image in images:
                imageUrls.append(image.get_attribute('src'))

        except Exception as e:
            print(e.__str__())

        data = {
            'description': description,
            'title': title,
            'price': '',
            'image': ','.join(imageUrls),
            'sku': ''
        }

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        ShannylightingScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
