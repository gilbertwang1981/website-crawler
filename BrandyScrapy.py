import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class BrandyScrapy(CommonScrapy):

    def getProductListByCategories(self):
        return [
            'https://brandy-designs.com/en-gb/catalog/Men-Fragrance-23',
            'https://brandy-designs.com/en-gb/catalog/Women-Fragrance',
            'https://brandy-designs.com/en-gb/catalog/fragrance',
            'https://brandy-designs.com/en-gb/catalog/brandy-minis/minis-men',
            'https://brandy-designs.com/en-gb/catalog/brandy-minis/minis-women',
            'https://brandy-designs.com/en-gb/catalog/brandy-minis/minis-unisex',
            'https://brandy-designs.com/en-gb/catalog/giftset-items'
        ]

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@id='product-list']"
                                    "//div[@class='banner-product']"
                                    "/a")
        urls = []
        for detail in details:
            urls.append(detail.get_attribute('href'))

        return list(set(urls))

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='product-name']").text
        except Exception as e:
            print(e.__str__())

        price = ''
        try:
            price = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='product-price']"
                                       "/span").text
        except Exception as e:
            print(e.__str__())

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//div[@id='flush-collapseOne']").text

            description = description + CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@id='flush-collapseTwo']").text
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance.\
                find_elements(By.XPATH, "//div[@id='carouselDemo']"
                                        "//div[@class='image']"
                                        "/a"
                                        "/img")
            for image in images:
                imageUrls.append(image.get_attribute('src'))

        except Exception as e:
            print(e.__str__())

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
        BrandyScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
