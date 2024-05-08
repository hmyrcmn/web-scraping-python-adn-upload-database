import scrapy
import json
import requests
from bs4  import BeautifulSoup as Soup

url="https://www.petlebi.com/kedi-urunleri/wanpy-karisik-sivi-kedi-odulu-14gr.html?recommended_by=dynamic&recommended_code=8a9eff68b327b2a00036fd32ea582314"

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

sayfa=requests.get(url,headers=headers)
icerik=Soup(sayfa.content,'html.parser')


urunfıyatı=icerik.find('div',{'class':'pd-price'}).get_text().strip() # fiyatların bulunduğu class için arama yapar.
print("fiyatı:",urunfıyatı)
