import CommonScrapyConfig
import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class InticosmeticScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categoryUrls = ['https://inticosmetic.com/produk/all/']

        return categoryUrls

    def getProductDetailByList(self):
        eTitles = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='dce-post-block']"
                                    "//div[@data-id='4fa8a81']"
                                    "//h2")

        urls = []
        for t in eTitles:
            urls.append(CommonScrapyConfig.commonScrapyConfig['scrapy']['initUrl'] + t.text.replace(' ', '-'))

        return urls

    def getProductDetail(self):
        title = ''
        description = ''
        imageUrl = ''

        try:
            title = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//h4[contains(@class, 'elementor-heading-title')]").text
        except Exception as e:
            e.__str__()

        try:
            description = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@data-id='c0d55da']").text
        except Exception as e:
            e.__str__()

        try:
            imageUrl = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@data-id='b913b0f']"
                                       "//img").get_attribute('src')
        except Exception as e:
            e.__str__()

        data = {
            'description': description,
            'title': title,
            'price': '',
            'image': imageUrl,
            'sku': ''
        }

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        InticosmeticScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
