import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class RiiffsperfumesScrapy(CommonScrapy):

    def getProductListByCategories(self):
        return ['https://www.riiffsperfumes.com/shop/']

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance.find_elements(By.XPATH,
                                                                                  "//li[contains(@class, 'product')]"
                                                                                  "//div[@class='product_item--info']"
                                                                                  "//a")
        urls = []
        for detail in details:
            pd = detail.get_attribute('href')
            if 'add-to-cart' in pd:
                pass
            else:
                urls.append(pd)

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance.find_element(By.XPATH,
                                                                                   "//h1[contains(@class, "
                                                                                   "'lakit-post-title ')]").text
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance.find_element(By.XPATH,
                                                                                         "//div[@id='tab-description']").text
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance.find_elements(By.XPATH,
                                                                                     "//div[contains(@class, "
                                                                                     "'lakit-product-images')] "
                                                                                     "//div[@data-thumb]")
            for image in images:
                img = image.get_attribute('data-thumb')
                imageUrls.append(img)

        except Exception as e:
            print(e.__str__())

        price = ""
        try:
            price = CommonScrapyProductService.chrome_driver_instance.find_element(By.XPATH, "//p[@class='price']").text
            price = price[:price.find("AED")]
        except Exception as e:
            e.__str__()

        return {
            'description': description,
            'title': title,
            'price': price,
            'image': ','.join(imageUrls)
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        RiiffsperfumesScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
