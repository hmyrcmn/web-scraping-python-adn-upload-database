import scrapy
import json
import requests
from bs4  import BeautifulSoup as Soup

url="https://www.petlebi.com/kedi-urunleri/wanpy-karisik-sivi-kedi-odulu-14gr.html?recommended_by=dynamic&recommended_code=8a9eff68b327b2a00036fd32ea582314"

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

sayfa=requests.get(url,headers=headers)
icerik=Soup(sayfa.content,'html.parser')

respon


urunfıyatı=icerik.find('div',{'class':'pd-price'}).get_text().strip() # fiyatların bulunduğu class için arama yapar.
print("fiyatı:",urunfıyatı)


product_name_element = icerik.find('h1', {'class': 'product-h1'}).get_text().strip()
print("product_name_element:",product_name_element)


urun_resmi_url = icerik.find('img')['src']
print("urun_resmi_url:",urun_resmi_url)


print("****************")

mytabcontent_element = icerik.find(id="hakkinda")  # id ve class ile elementi bulun


marka_element = mytabcontent_element.find("div", class_="col-10 pd-d-v").text.strip()
barkod_element = mytabcontent_element.find_all("div", class_="col-10 pd-d-v")[1].text.strip()
skt = mytabcontent_element.find_all("div", class_="col-10 pd-d-v")[1].text.strip()

print("Marka:", marka_element)
print("Barkod:", barkod_element)
print("skt:",skt)


print("--****************")
quantity_dropdown = icerik.find(id="quantity")

max_option_value = None
for option in quantity_dropdown.find_all("option"):
  value = option.get("value")
  if value and (not max_option_value or int(value) > int(max_option_value)):
    max_option_value = value
    
print("stok:",max_option_value)
print("***********")

# "pp-bestseller" elementini bul
bestseller_element = icerik.find("div", class_="pp-bestseller")

# "a" etiketini bul
link_element = bestseller_element.find("a")

# Ürün linkini ve adını al
urun_linki = link_element["href"]
urun_adi = link_element.text.strip()

# Ürün kategorisi ve satış sıralaması metnini al
kategori_metni = bestseller_element.text.strip()

# Kategoriyi ve satış sıralamasını ayıkla
kategori = kategori_metni.split("kategorisinde")[0].strip()
satis_siralamasi = kategori_metni.split("en çok satılan")[1].strip()

# Sonuçları yazdır
print("Ürün Adı:", urun_adi)
print("Ürün Linki:", urun_linki)
print("Kategori:", kategori)
print("Satış Sıralaması:", satis_siralamasi)