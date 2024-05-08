import scrapy


class PetlebiSpider(scrapy.Spider):
    name = "petlebi"
    start_urls = ["https://www.petlebi.com/"]

    def parse(self, response):
        # Ürünlerin bulunduğu HTML elementlerini seç
        products = response.css(".product-item")

        # Her ürün için JSON nesnesi oluştur
        for product in products:
            yield {
                "url": product.css(".product-image a::attr(href)").get(),
                "name": product.css(".product-name a::text").get(),
                "barcode": product.css(".product-barcode::text").get(),
                "price": product.css(".product-price::text").get(),
                "stock": product.css(".product-stock::text").get(),
                "images": [
                    image.css("::attr(src)").get()
                    for image in product.css(".product-images img")
                ],
                "description": product.css(".product-description::text").get(),
                "sku": product.css(".product-sku::text").get(),
                "category": product.css(".product-category::text").get(),
                "product_id": product.css(".product-id::text").get(),
                "brand": product.css(".product-brand::text").get(),
            }

        # Sayfalama varsa diğer sayfalara da git
        next_page = response.css(".pagination a.next::attr(href)").get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

