import scrapy

class PetlebiSpider(scrapy.Spider):
    name = "petlebi"
    allowed_domains = ["petlebi.com"]
    start_urls = ["https://www.petlebi.com/kopek-urunleri/pro-plan-duo-delice-parca-etli-biftekli-yetiskin-kopek-mamasi-10kg.html?page=1#yorumlar"]

    def parse(self, response):
       url_xpath = '//div[@class="col-md-6 col-sm-5"]/a/@href'
        name_xpath = '//h1[@class="product-h1"]/text()'
        rating_xpath = '//span[@id="puan"]/span/text()'
        comment_count_xpath = '//span[@class="product-rating"]/span[@class="comments-count"]/text()'
        price_xpath = '//span[@class="new-price"]/text()'
        old_price_xpath = '//del[@class="old-price"]/text()'
        cargo_free_xpath = '//span[@class="bg-light rounded pd-badge pd-cargofree-badge mb-2"]/text()'
        promotion_image_xpath = '//fieldset[@class="pd-promotions"]//a[@class="thumb-link mz-show-arrows mz-thumb"]/img/@src'
        best_before_xpath = '//span[@class="pdbestbefore"]/strong/text()'
        shipping_time_xpath = '//span[@id="shippingClock"]/text()'
        image_xpath = '//div[@class="mcs-item"]//a[@class="thumb-link mz-thumb-selected mz-show-arrows mz-thumb"]/@data-image'

        # XPath ifadelerini kullanarak bilgileri çıkar
        productURL = response.xpath(url_xpath).extract_first()
        ProductName = response.xpath(name_xpath).extract_first()
        rating = response.xpath(rating_xpath).extract_first()
        comment_count = response.xpath(comment_count_xpath).extract_first()
        price = response.xpath(price_xpath).extract_first()
        old_price = response.xpath(old_price_xpath).extract_first()
        cargo_free = response.xpath(cargo_free_xpath).extract_first()
        promotion_image = response.xpath(promotion_image_xpath).extract()
        best_before = response.xpath(best_before_xpath).extract_first()
        shipping_time = response.xpath(shipping_time_xpath).extract_first()
        images = response.xpath(image_xpath).extract()
            yield {
                'ürün url: ':productURL,
                'ürün adı:': ProductName,
                'ürün id:':ProductID,
                'urun fiyatı:':productPrice,
                'indirimsiz fiyat:':productPriceNotDiscount,
                'ürün resmi:.':productImageURL,
                'son kullanma  tarihi:':expirationDate,
                'categroy:':category,
                'marka:':productBrand
                
            }
