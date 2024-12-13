import CommonScrapyProductService
from CommonScrapy import CommonScrapy


class AtcacarScrapy(CommonScrapy):
    def __init__(self, chromeDriver):
        self.chrome = chromeDriver

    def getProductListByCategories(self):
        return ['https://shop.atcacar.com/product-category/automotive-accessories/audio-electronics/']

    def getProductDetailByList(self):
        return ['https://shop.atcacar.com/product/air-compressor-635-double-cylinder-85l/']

    def getProductDetail(self):
        return {
            'description': 'test description',
            'title': 'this is a product',
            'price': '10',
            'image': 'xxxx'
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(AtcacarScrapy(CommonScrapyProductService.getChromeDriver()))

    CommonScrapyProductService.closeChromeDriver()
