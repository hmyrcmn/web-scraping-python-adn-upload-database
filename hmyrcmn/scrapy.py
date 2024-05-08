import scrapy

class PetlebiSpider(scrapy.Spider):
    name = "petlebi"
    allowed_domains = ["petlebi.com"]
    
    def start_requests(self):
        # İlk sayfadan başlayarak tüm sayfaların URL'lerini oluştur
        base_url = "https://www.petlebi.com/kedi-mamasi?page={}"
        for page_number in range(1, 101):  # 100 sayfa olduğunu varsayalım, istediğiniz sayıya göre değiştirin
            yield scrapy.Request(base_url.format(page_number), callback=self.parse)

    def parse(self, response):
        # Sayfa yüklendiğindeki popüler ürünlerin bağlantılarını alın
        populerProducts = response.xpath("//div[@class='row listitempage']/div/div")
        for populerProduct in populerProducts:
            productURL = populerProduct.xpath('.//div[@class="card-body pb-0 pt-2 pl-3 pr-3"]/a/@href').get()
            ProductID = populerProduct.xpath('.//div[@class="card-body pb-0 pt-2 pl-3 pr-3"]/a/@id').get()
            productCategory = populerProduct.xpath('.//a[@class="p-link"]/@data-gtm-product').get()
            if productCategory:
                productCategory = productCategory.split('"category":"')[1].split('","')[0]

            yield scrapy.Request(productURL, callback=self.parse_product_page, meta={'ProductID': ProductID, 'url': productURL, 'productCategory': productCategory})

    def parse_product_page(self, response):
        # Ürün sayfasından gerekli bilgileri çekin ve yield edin
        ProductName = response.xpath('//h1[@class="product-h1"]/text()').get()
        productPrice = response.xpath('//div[@class="col-8 pd-price"]/p/span[@class="new-price"]/text()').get()
        productPriceNotDiscount = response.xpath('//div[@class="col-8 pd-price"]/p/del/text()').get()
        productImageURL = response.xpath('//div[@class="col-md-6 col-sm-5"]/div/a/img/@src').get()
        barkod = response.xpath('//div[@id="myTabContent"]//div[text()="BARKOD"]/following-sibling::div/text()').get().strip()
        skt = response.xpath('//div[@id="myTabContent"]//div[text()="S.K.T."]/following-sibling::div/text()').get()
        marka = response.xpath('//div[@id="hakkinda"]//div[@class="row mb-2 brand-line"]/div[@class="col-10 pd-d-v"]/span/a/text()').get()
        stok = response.xpath('//select[@id="quantity"]/option[last()]/text()').get()
        productDescription = response.xpath('//span[@id="productDescription"]/p/text()').get()
        productURL = response.url

        yield {
            'ürün adı:': ProductName,
            'urun fiyatı:': productPrice,
            'indirimsiz fiyat:': productPriceNotDiscount,
            'ürün resmi:.': productImageURL,
            'ürün url:': productURL,
            'barkod: ': barkod,
            'skt:': skt,
            'marka:': marka,
            'stok adedi:': stok,
            'ürün acıklama:': productDescription,
            'ürün id:': response.meta['ProductID'],
            'category:': response.meta['productCategory']
        }
