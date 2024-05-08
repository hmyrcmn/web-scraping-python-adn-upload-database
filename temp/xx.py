print("hello")

import sys
sys.path.append("C:\\python312\\lib\\site-packages")
import scrapy 
import subprocess


print("version ",scrapy.__version__)

class MySpider(scrapy.Spider):
    name = "myspider"
    
    def start_requests(self):
        #yield from self.make_requests_from_url(url)
        
        urls=["https://www.petlebi.com"]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        filename="output.html"
        with open(filename,"wb") as f:
            f.write(response.body)
            print(f"Saved file {filename} ")
        self.log('Saved file "{}"'.format(filename))
        #yield {'file_contents': response.text}

def runspider():
    process = subprocess.Popen(['scrapy', 'crawl','myspider'], stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            line = output.strip().decode()
            print(line)

if __name__=="__main__":
    runspider() 
