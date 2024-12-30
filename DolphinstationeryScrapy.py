import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class DolphinstationeryScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categories = CommonScrapyProductService.chrome_driver_instance.\
            find_elements(By.XPATH, "//div[@id='ContentPlaceHolder1_PanelAltGruplar']"
                                    "//a")

        categoryUrls = []
        for category in categories:
            categoryUrl = category.get_attribute('href')
            categoryUrls.append(categoryUrl)

        return list(set(categoryUrls))

    def getProductDetailByList(self):
        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@id='ContentPlaceHolder1_PanelUrunler']"
                                    "//a")
        urls = []
        for detail in details:
            detailUrl = detail.get_attribute('href')
            urls.append(detailUrl)

        return list(set(urls))

    def getProductDetail(self):
        title = ''
        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance.\
                find_element(By.XPATH, "//h4[text()='Product Info']/following-sibling::h4[1]").text

            title = description.split('\n')[0]
        except Exception as e:
            print(e.__str__())

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance.\
                find_elements(By.XPATH, "//div[@id='gallery1']"
                                        "//a")
            for image in images:
                imageUrls.append(image.get_attribute('href'))

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
        DolphinstationeryScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
