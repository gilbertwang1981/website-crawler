import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class MebashiScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categoryUrls = [
            'https://www.mebashi.com/products'
        ]

        return categoryUrls

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='product_item_card']"
                                    "/div[@class='product_item_body']"
                                    "/a")

        detailsUrls = []
        for detail in details:
            print(detail.get_attribute('href'))
            detailsUrls.append(detail.get_attribute('href'))

        print(len(detailsUrls))

        return detailsUrls

    def getProductDetail(self):
        title = ''
        description = ''
        imageUrls = []

        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'product_details_info')]"
                                       "//h3").text
        except Exception as e:
            e.__str__()

        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'product_details_info')]"
                                       "//ul[@class='highlights_area']").text

            description = description + CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'product_details_info')]"
                                       "//div[@class='info_wrapper']"
                                       "//p").text
        except Exception as e:
            e.__str__()

        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[contains(@class, 'product_details_image_gallery ')]"
                                        "//div[contains(@class, 'slick-track')]"
                                        "/div[contains(@class, 'slick-slide')]"
                                        "/div"
                                        "/a")

            for image in images:
                img = image.get_attribute('href')
                if "javascript" not in img:
                    imageUrls.append(img)
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
        MebashiScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
