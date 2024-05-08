import json
import psycopg2
from psycopg2 import Error

# .env dosyasından veritabanı bağlantı bilgilerini al
import os
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# PostgreSQL veritabanına bağlanma
try:
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    print("Bağlantı başarılı")

    cursor = connection.cursor()

    # Tabloyu oluşturma sorgusu
    create_table_query = """
    CREATE TABLE IF NOT EXISTS mypetlebi2 (
        id SERIAL PRIMARY KEY,
        urun_adi VARCHAR(255),
        urun_fiyati VARCHAR(50),
        indirimsiz_fiyat VARCHAR(50),
        urun_resmi VARCHAR(255),
        urun_url VARCHAR(255),
        barkod VARCHAR(50),
        skt DATE,
        marka VARCHAR(100),
        stok_adedi VARCHAR(50),
        urun_aciklama TEXT,
        urun_id VARCHAR(50),
        category VARCHAR(255)
    )
    """
    
    # Tabloyu oluştur
    cursor.execute(create_table_query)
    connection.commit()
    print("Tablo başarıyla oluşturuldu")

    # JSON dosyasını oku
    
    with open('lastUpdate/xx.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            # SQL sorgusu
            sql_query = """INSERT INTO mypetlebi2 (urun_adi, urun_fiyati, indirimsiz_fiyat, urun_resmi, 
                                                urun_url, barkod, skt, marka, stok_adedi, urun_aciklama, 
                                                urun_id, category) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            # JSON verilerini tabloya ekle
            cursor.execute(sql_query, (item['ürün adı'], item['urun fiyatı'], item['indirimsiz fiyat'],
                                       item['ürün resmi'], item['ürün url'], item['barkod'],
                                       item['skt'], item['marka'], item['stok adedi'],
                                       item['ürün acıklama'], item['ürün id'], item['kategori']))

    # Değişiklikleri kaydet
    connection.commit()
    print("Veriler başarıyla eklendi")

except (Exception, Error) as error:
    print("Bağlantı hatası:", error)

finally:
    # Bağlantıyı kapatma
    if connection:
        cursor.close()
        connection.close()
        print("Bağlantı kapatıldı")
