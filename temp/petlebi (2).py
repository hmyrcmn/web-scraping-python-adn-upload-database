import scrapy

class PetlebiSpider(scrapy.Spider):
    name = "petlebi"
    allowed_domains = ["petlebi.com"]
    start_urls = ["https://www.petlebi.com"]

    def parse(self, response):
        # Ana sayfadaki tüm bölümleri al
        sections = response.xpath('//nav[@class="wsmenu clearfix"]/ul/li')
        
        # Her bir bölüm için içindeki linkleri al
        for section in sections:
            links = section.xpath('.//div/ul/li/a')
            
            # Her bir link için URL ve metin içeriğini al
            for link in links:
                url = link.xpath('./@href').get()
            
                # JavaScript URL'lerini filtrele
                if url and not url.startswith('javascript:'):
                    yield scrapy.Request(url, callback=self.parse_product_page)
        
        # # Sayfa numaralarını takip et
        # next_page = response.xpath("//li[@class='page-item']/a[@rel='next']/@href").get()
        # if next_page:
        #     yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_product_page(self, response):
        # Sayfadaki popüler ürünlerin bilgilerini al
        products = response.xpath("//div[@class='row listitempage']/div/div")
        for product in products:
            productURL = product.xpath('.//div[@class="card-body pb-0 pt-2 pl-3 pr-3"]/a/@href').get()
            ProductID = product.xpath('.//div[@class="card-body pb-0 pt-2 pl-3 pr-3"]/a/@id').get()
            productCategory = product.xpath('.//a[@class="p-link"]/@data-gtm-product').get()
            if productCategory:
                productCategory = productCategory.split('"category":"')[1].split('","')[0]

            yield scrapy.Request(productURL, callback=self.parse_product_details, meta={'ProductID': ProductID, 'url': productURL, 'productCategory': productCategory})
              # Sayfa numaralarını takip et
            next_page = response.xpath("//li[@class='page-item']/a[@rel='next']/@href").get()
            if next_page:
                yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_product_details(self, response):
        # Ürün sayfasından gerekli bilgileri çekin ve yield edin
        ProductName = response.xpath('//h1[@class="product-h1"]/text()').get()
        productPrice = response.xpath('//div[@class="col-8 pd-price"]/p/span[@class="new-price"]/text()').get()
        productPriceNotDiscount = response.xpath('//div[@class="col-8 pd-price"]/p/del/text()').get()
        productImageURL = response.xpath('//div[@class="col-md-6 col-sm-5"]/div/a/img/@src').get()
        barkod = response.xpath('//div[@id="myTabContent"]//div[text()="BARKOD"]/following-sibling::div/text()').get()
        if barkod:
            barkod = barkod.strip()
        skt = response.xpath('//div[@id="myTabContent"]//div[text()="S.K.T."]/following-sibling::div/text()').get()
        marka = response.xpath('//div[@id="hakkinda"]//div[@class="row mb-2 brand-line"]/div[@class="col-10 pd-d-v"]/span/a/text()').get()
        stok = response.xpath('//select[@id="quantity"]/option[last()]/text()').get()
        productDescription = response.xpath('//span[@id="productDescription"]/p/text()').get()
        productURL = response.url

        yield {
            'ürün adı': ProductName,
            'urun fiyatı': productPrice,
            'indirimsiz fiyat': productPriceNotDiscount,
            'ürün resmi': productImageURL,
            'ürün url': productURL,
            'barkod': barkod,
            'skt': skt,
            'marka': marka,
            'stok adedi': stok,
            'ürün acıklama': productDescription,
            'ürün id': response.meta.get('ProductID'),
            'kategori': response.meta.get('productCategory')
        }
