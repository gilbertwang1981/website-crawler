import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class MktgroupScrapy(CommonScrapy):

    def __init__(self):
        self.titles = []
        self.descriptions = []
        self.imageUrls = []
        self.index = 0

    def getProductListByCategories(self):
        categoryUrls = ['https://www.mktgroup.ae/detail.php?Cid=&PtId=R',
                        'https://www.mktgroup.ae/detail.php?Cid=&PtId=F',
                        'https://www.mktgroup.ae/detail.php?Cid=&PtId=NF',
                        'https://www.mktgroup.ae/details.php?Cid=RI&PtId=C',
                        'https://www.mktgroup.ae/detail.php?Cid=&PtId=DS']

        return categoryUrls

    def getProductDetailByList(self):
        eTitles = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='about-info']"
                                    "//div[@class='card']"
                                    "/h5[1]")

        eDesc = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='about-info']"
                                    "//div[@class='card']"
                                    "/h5[2]")

        images = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[@class='about-info']"
                                    "//div[@class='card']"
                                    "/img")

        urls = []
        count = 0
        for title in eTitles:
            urls.append(CommonScrapyProductService.
                        chrome_driver_instance.current_url)

            self.titles.append(title.text)
            self.descriptions.append(eDesc[count].text)
            self.imageUrls.append(images[count].get_attribute('src'))

            count = count + 1

        return urls

    def getProductDetail(self):
        data = {
            'description': self.descriptions[self.index],
            'title': self.titles[self.index],
            'price': '',
            'image': self.imageUrls[self.index],
            'sku': ''
        }

        self.index = self.index + 1

        print(data)

        return data


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        MktgroupScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
