import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class GracekitcheScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categoryUrls = []

        categories = CommonScrapyProductService.chrome_driver_instance.\
            find_elements(By.XPATH, "//div[contains(@class, 'products')]"
                                    "/div"
                                    "//div[@class='category-image-wrapp']"
                                    "/a")
        for category in categories:
            categoryUrls.append(category.get_attribute('href'))

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[contains(@class, 'wd-product')]"
                                    "/div[@class='product-wrapper']"
                                    "/div"
                                    "/a")

        detailsUrls = []
        for detail in details:
            detailsUrls.append(detail.get_attribute('href'))

        return detailsUrls

    def getProductDetail(self):
        title = ''
        description = ''
        imageUrls = []

        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'product-image-summary-inner')]"
                                       "/div[contains(@class, 'summary')]"
                                       "/div"
                                       "/h1[contains(@class, 'product_title')]").text
        except Exception as e:
            e.__str__()

        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@class='woocommerce-product-details__short-description']").text
        except Exception as e:
            e.__str__()

        try:
            image = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'product-images')]"
                                       "/div[contains(@class, 'woocommerce-product-gallery')]"
                                       "/div[contains(@class, 'wd-gallery-images')]"
                                       "//a")
            if image:
                imageUrls.append(image.get_attribute('href'))

            imgDesc = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[@class='product-tabs-wrapper']"
                                        "//div[@id='tab-description']"
                                        "//img")

            for img in imgDesc:
                imageUrls.append(img.get_attribute('src'))

        except Exception as e:
            e.__str__()

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
        GracekitcheScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
