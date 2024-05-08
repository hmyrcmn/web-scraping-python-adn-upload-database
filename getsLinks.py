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
                text = link.xpath('./text()').get()
                print("URL:", url)
                print("Text:", text)