import sys
sys.path.append("C:\\python312\\lib\\site-packages")
import scrapy 
import json
import scrapy
from scrapy_selenium import SeleniumRequest

class PetlebiSpider(scrapy.Spider):
    name = "petlebi"
    start_urls = [
        "https://www.petlebi.com/"
    ]

    def parse(self, response):
        # JavaScript ile yüklenen ürünlerin render edilmesini bekleyin
        yield SeleniumRequest(
            url=response.url,
            wait_until="domcontentloaded",
            callback=self.parse_products,
        )

    def parse_products(self, response):
        products = response.css(".product-item")
        for product in products:
            yield {
                
                "product_price": product.css(".pd-price::text").get(),
                "product_stock": product.css(".product-stock::text").get(),
                "product_images": product.css(".product-images img::attr(src)").getall(),
                "description": product.css(".product-description::text").get(),
                "sku": product.css(".product-sku::text").get(),
                "category": product.css(".product-category::text").get(),
                "product_id": product.css(".product-id::text").get(),
                "brand": product.css(".product-brand::text").get(),
            }

# JSON dosyasına yazma işlemi
def write_to_json(data):
    with open('petlebi_products.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Spider'ı çalıştırma
def run_spider():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'petlebi_products.json',
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_PATH': 'C:\\Users\\HÜMEYRA\\Downloads\\chromedriver_win32\\chromedriver.exe',
        'USER_AGENT': 'Mozilla/5.0'
    })
    process.crawl(PetlebiSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
