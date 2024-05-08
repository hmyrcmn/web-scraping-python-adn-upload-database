CREATE TABLE mypetlebi2 (
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
);
