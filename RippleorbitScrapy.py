import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class RippleorbitScrapy(CommonScrapy):

    def getProductListByCategories(self):
        # categories = CommonScrapyProductService. \
        #     chrome_driver_instance.find_elements(By.XPATH,
        #                                          "//ul[@class='xg_tMenuUl1']/li")
        # urls = []
        # for category in categories:
        #     categoryId = category.get_attribute('data-tid')
        #     urls.append("http://www.rippleorbit.com/sv.aspx?nid=8&typeid=" + str(categoryId))

        # return urls

        return ['http://www.rippleorbit.com/sv_complex.aspx?nid=8']

    def getProductDetailByList(self):
        details = CommonScrapyProductService. \
            chrome_driver_instance.find_elements(By.XPATH,
                                                 "//div[contains(@class, "
                                                 "'xg_content')]"
                                                 "//div[contains(@class, 'data_row')]"
                                                 "//a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return list(set(urls))

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
