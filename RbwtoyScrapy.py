import CommonScrapyProductService
from CommonScrapy import CommonScrapy
from selenium.webdriver.common.by import By


class RbwtoyScrapy(CommonScrapy):

    def getProductListByCategories(self):
        categoryUrls = [
            'https://rbwtoy.com/Outdoor-Play-Toys/Outdoor-new-models',
            'https://rbwtoy.com/Outdoor-Play-Toys/Outdoor-Play-Ground',
            'https://rbwtoy.com/Outdoor-Play-Toys/Seesaws-new-models',
            'https://rbwtoy.com/Outdoor-Play-Toys/Seesaws-Rounder-toys',
            'https://rbwtoy.com/Outdoor-Play-Toys/slide-and-swing-sets-for-kids',
            'https://rbwtoy.com/Outdoor-Play-Toys/Trampolines',
            'https://rbwtoy.com/Outdoor-Play-Toys/Water-Play-Ground-toys',
            'https://rbwtoy.com/Education-Series-toys/Table-chairs-kids',
            'https://rbwtoy.com/Education-Series-toys/White-Boards',
            'https://rbwtoy.com/Wooden-Series/wooden-benches',
            'https://rbwtoy.com/Wooden-Series/Wooden-Cabinet',
            'https://rbwtoy.com/Wooden-Series/Wooden-Trash-bin',
            'https://rbwtoy.com/Wooden-Series/Wooden-doll-house',
            'https://rbwtoy.com/Wooden-Series/Wooden-kitchen-set',
            'https://rbwtoy.com/Seesaws-new-models',
            'https://rbwtoy.com/indoor-toys',
            'https://rbwtoy.com/Wooden-Series/Wooden-doll-house',
            'https://rbwtoy.com/Wooden-Series/Wooden-kitchen-set',
            'https://rbwtoy.com/soft-toys',
            'https://rbwtoy.com/Fitness-toys/Kids-physical-toys',
            'https://rbwtoy.com/Outdoor-Play-Toys/Water-Play-Ground-toys',
            'https://rbwtoy.com/indoor-toys/Seesaws-Plastic',
            'https://rbwtoy.com/indoor-toys/kids-playhouse',
            'https://rbwtoy.com/Fitness-toys/Kids-physical-toys',
            'https://rbwtoy.com/Fitness-toys/kids-fitness',
            'https://rbwtoy.com/soft-toys',
            'https://rbwtoy.com/Education-Series-toys/Table-chairs-kids',
            'https://rbwtoy.com/soft-toys/Soft-indoor',
            'https://rbwtoy.com/Fitness-toys/kids-fitness',
            'https://rbwtoy.com/Fitness-toys',
            'https://rbwtoy.com/Education-Series-toys',
            'https://rbwtoy.com/Fitness-toys',
            'https://rbwtoy.com/Fitness-toys/Kids-physical-toys',
            'https://rbwtoy.com/soft-toys/Soft-indoor',
            'https://rbwtoy.com/Education-Series-toys/Table-chairs-kids',
            'https://rbwtoy.com/Outdoor-Play-Toys/Water-Play-Ground-toys',
            'https://rbwtoy.com/indoor-toys/Plastic-Toys-New-Models'
        ]

        return list(set(categoryUrls))

    def getProductDetailByList(self):

        details = CommonScrapyProductService.chrome_driver_instance. \
            find_elements(By.XPATH, "//div[contains(@class, 'product-grid')]"
                                    "//div[@class='product-image-container']"
                                    "/a")
        urls = []
        for detail in details:
            if "quickview" not in detail.get_attribute('href'):
                urls.append(detail.get_attribute('href'))

        return urls

    def getProductDetail(self):
        title = ''
        try:
            title = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH,
                             "//div[@class='title-product']"
                             "/h1").text
        except Exception as e:
            e.__str__()

        description = ''
        try:
            description = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[@id='tab-description']").text
        except Exception as e:
            e.__str__()

        price = ''
        try:
            price = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'product_page_price')]"
                                       "//span[@id='price-old']").text
        except Exception as e:
            e.__str__()

        sku = ''
        try:
            sku = CommonScrapyProductService.chrome_driver_instance. \
                find_element(By.XPATH, "//div[contains(@class, 'inner-box-desc')]"
                                       "/div[@class='model']").text

            sku = sku.split(':')[1].strip()
        except Exception as e:
            e.__str__()

        imageUrls = []
        try:
            images = CommonScrapyProductService.chrome_driver_instance. \
                find_elements(By.XPATH, "//div[@id='thumb-slider']"
                                        "//div[@class='image-additional']"
                                        "/a")

            for image in images:
                imageUrls.append(image.get_attribute('data-image'))

        except Exception as e:
            e.__str__()

        return {
            'description': description,
            'title': title,
            'price': price,
            'image': ','.join(imageUrls),
            'sku': sku
        }


if __name__ == '__main__':
    CommonScrapyProductService.createChromeDriver()

    CommonScrapyProductService.listProducts(
        RbwtoyScrapy(),
        CommonScrapyProductService.getProductListPageSize())

    CommonScrapyProductService.closeChromeDriver()
