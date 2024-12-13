import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class RippleorbitScrapy(CommonScrapy):

    def getProductListByCategories(self):
        return ['http://www.rippleorbit.com/sv_complex.aspx?nid=8']

    def getProductDetailByList(self):
        details = CommonScrapyProductService. \
            chrome_driver_instance.find_elements(By.XPATH,
                                                 "//div[@id='idccf372c42914471']"
                                                 "//div[contains(@class, 'data_col')]"
                                                 "//a[1]")
        urls = set([])
        for detail in details:
            urls.add(detail.get_attribute('href'))

        return list(urls)

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService. \
                chrome_driver_instance.find_element(By.XPATH,
                                                    "//div[@class='xg_content']"
                                                    "//div[@class='container'][1]"
                                                    "//div[contains(@class, 'col-lg-12')]"
                                                    "//div[contains(@class, 'col-lg-7')]"
                                                    "//div[contains(@class, 'xg_text')]/span").text
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService. \
                chrome_driver_instance.find_element(By.XPATH,
                                                    "//div[@class='xg_content']"
                                                    "//div[@class='container'][1]"
                                                    "//div[contains(@class, 'col-lg-12')]"
                                                    "//div[contains(@class, 'col-lg-7')]").text
        except Exception as e:
            print(e.__str__())

        try:
            image = CommonScrapyProductService. \
                chrome_driver_instance.find_element(By.XPATH,
                                                    "//div[@class='xg_content']"
                                                    "//div[@class='container'][1]"
                                                    "//div[contains(@class, 'col-lg-12')]"
                                                    "//div[contains(@class, 'col-lg-5')]"
                                                    "//div[contains(@class, 'col-lg-12')]"
                                                    "//img")

            productImages = image.get_attribute('data-src')

        except Exception as e:
            print(e.__str__())

        return {
            'description': description,
            'title': title,
            'price': "",
            'image': productImages
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        RippleorbitScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
