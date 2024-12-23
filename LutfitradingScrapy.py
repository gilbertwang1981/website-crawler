import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class LutfitradingScrapy(CommonScrapy):

    def __init__(self):
        self.categoriesList = []

    def addCategoriesInList(self):
        categories = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='collection-list__section']"
                                    "//div[@class='grid']"
                                    "//a[contains(@class, 'collection-block-item')]")
        for category in categories:
            self.categoriesList.append(category.get_attribute('href'))

    def getProductListByCategories(self):
        self.addCategoriesInList()

        CommonScrapyProductService.chrome_driver_instance.get('https://lutfitrading.com/collections?page=2')

        self.addCategoriesInList()

        return self.categoriesList

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[contains(@class, 'product-list')]"
                                    "/div[contains(@class, 'product-item')]"
                                    "/a")

        detailsUrls = []
        for detail in details:
            detailsUrls.append(detail.get_attribute('href'))

        return detailsUrls

    def getProductDetail(self):

        title = ''
        price = ''
        description = ''
        imageUrls = []

        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'product-meta')]"
                                       "/h1[contains(@class, 'product-meta__title')]").text
        except Exception as e:
            e.__str__()

        try:
            price = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='price-list']"
                                       "//span[@class='price']").text
        except Exception as e:
            e.__str__()

        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'product-block-list__item--description')]"
                                       "//div[@class='card__section ']").text
        except Exception as e:
            e.__str__()

        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[contains(@class, 'product-gallery__carousel-item ')]"
                                        "//img[contains(@class, 'product-gallery__image')]")

            for image in images:
                imageUrls.append(image.get_attribute('data-zoom').split('?')[0])
        except Exception as e:
            e.__str__()

        data = {
            'description': description,
            'title': title,
            'price': price,
            'image': ','.join(imageUrls),
            'sku': ''
        }

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        LutfitradingScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
