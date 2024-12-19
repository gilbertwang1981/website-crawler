import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class TitastarScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categoryUrls = [
            'https://www.titastar.com/hybrid-inverters/twin-series/',
            'https://www.titastar.com/ts-pro-max-series-2-2kw/3-2kw/4-2kw/6-2kw/7kw/10-2kw/',
            'https://www.titastar.com/ts-solar-battery-gel-agm-tubler-battery/',
            'https://www.titastar.com/ts-solar-lithium-ion-battery/',
            'https://www.titastar.com/solar-street-lights/solar-street-light-bct-olc-1-0/',
            'https://www.titastar.com/solar-panels/standrad-solar-panel-monos/',
            'https://www.titastar.com/solar-charge-controllers/',
            'https://www.titastar.com/solar-air-conditioner/'
        ]

        return list(set(categoryUrls))

    def getProductDetailByList(self):

        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//ul[@id='prodListingContainer']"
                                    "/li[@class='listpager']"
                                    "//div[@class='p-txt-ar']"
                                    "/p[@class='p-hd']"
                                    "/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH,
                             "//div[@class='detail_sec']"
                             "/h1").text
            print(title)
        except Exception as e:
            e.__str__()

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@id='d1']").text

            print(description)
        except Exception as e:
            e.__str__()

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[@class='pc_box']"
                                        "//div[@class='ds_thm']"
                                        "//a")

            for image in images:
                imageUrls.append(image.get_attribute('href'))

            print(imageUrls)
            print("")

        except Exception as e:
            e.__str__()

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
        TitastarScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
