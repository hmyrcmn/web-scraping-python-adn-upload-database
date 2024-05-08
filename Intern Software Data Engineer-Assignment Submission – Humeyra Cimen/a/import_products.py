import mysql.connector
import json 
def import_products(products):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Humeyra.106",
        database="petlebi",
    )
    cursor = connection.cursor()

    for product in products:
        cursor.execute(
            """
            INSERT INTO petlebi (
                url,
                name,
                barcode,
                price,
                stock,
                images,
                description,
                sku,
                category,
                product_id,
                brand
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                product["url"],
                product["name"],
                product["barcode"],
                product["price"],
                product["stock"],
                json.dumps(product["images"]),
                product["description"],
                product["sku"],
                product["category"],
                product["product_id"],
                product["brand"],
            ),
        )

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    with open("petlebi_products.json", "r") as f:
        products = json.load(f)

    import_products(products)

