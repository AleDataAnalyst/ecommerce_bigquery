from google.cloud import bigquery
from src.config import get_bigquery_client, DATASET_ID

def create_dataset():
    client = get_bigquery_client()
    dataset_ref = f"{client.project}.{DATASET_ID}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "EU"
    client.create_dataset(dataset, exists_ok=True)
    print(f"✅ Dataset {DATASET_ID} verificado/creado.")

def create_tables():
    client = get_bigquery_client()
    
    # Esquemas siguiendo 3NF
    schemas = {
        "categories": [
            bigquery.SchemaField("category_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("description", "STRING")
        ],
        "products": [
            bigquery.SchemaField("product_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("category_id", "INTEGER"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("price", "FLOAT"),
            bigquery.SchemaField("cost", "FLOAT"),
            bigquery.SchemaField("stock", "INTEGER"),
            bigquery.SchemaField("is_active", "BOOLEAN")
        ],
        "customers": [
            bigquery.SchemaField("customer_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("country", "STRING"),
            bigquery.SchemaField("city", "STRING"),
            bigquery.SchemaField("acquisition_channel", "STRING"),
            bigquery.SchemaField("registration_date", "DATE")
        ],
        "orders": [
            bigquery.SchemaField("order_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "INTEGER"),
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("order_date", "DATETIME"),
            bigquery.SchemaField("shipping_date", "DATETIME"),
            bigquery.SchemaField("delivery_date", "DATETIME")
        ],
        "order_items": [
            bigquery.SchemaField("order_item_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("order_id", "INTEGER"),
            bigquery.SchemaField("product_id", "INTEGER"),
            bigquery.SchemaField("quantity", "INTEGER"),
            bigquery.SchemaField("unit_price", "FLOAT"), # Snapshot del precio al comprar (3NF)
            bigquery.SchemaField("discount", "FLOAT")
        ],
        "payments": [
            bigquery.SchemaField("payment_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("order_id", "INTEGER"),
            bigquery.SchemaField("payment_method", "STRING"),
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("amount", "FLOAT"),
            bigquery.SchemaField("payment_date", "DATETIME")
        ],
        "reviews": [
            bigquery.SchemaField("review_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("order_item_id", "INTEGER"),
            bigquery.SchemaField("rating", "INTEGER"),
            bigquery.SchemaField("comment", "STRING")
        ]
    }

    for table_name, schema in schemas.items():
        table_ref = f"{client.project}.{DATASET_ID}.{table_name}"
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table, exists_ok=True)
        print(f"✅ Tabla {table_name} creada con éxito.")

if __name__ == "__main__":
    create_dataset()
    create_tables()