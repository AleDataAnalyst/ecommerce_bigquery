from google.cloud import bigquery
from src.config import get_bigquery_client, DATASET_ID

def load_dataframe_to_bigquery(df, table_name):
    client = get_bigquery_client()
    table_ref = f"{client.project}.{DATASET_ID}.{table_name}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # Sobrescribe los datos si ya existen (ideal para recargas de prueba)
    )
    
    try:
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Esperar a que termine el proceso de carga
        print(f"✅ Tabla '{table_name}' cargada con éxito: {len(df)} filas insertadas en BigQuery.")
    except Exception as e:
        print(f"❌ Error al cargar la tabla '{table_name}': {e}")

if __name__ == "__main__":
    from src.generate_data import generate_synthetic_data
    
    # Generar datos y cargarlos en orden de dependencias lógicas
    data = generate_synthetic_data()
    
    # Orden crítico para respetar claves ajenas (aunque BigQuery no las fuerza, es una buena práctica operativa)
    load_dataframe_to_bigquery(data["categories"], "categories")
    load_dataframe_to_bigquery(data["products"], "products")
    load_dataframe_to_bigquery(data["customers"], "customers")
    load_dataframe_to_bigquery(data["orders"], "orders")
    load_dataframe_to_bigquery(data["order_items"], "order_items")
    load_dataframe_to_bigquery(data["payments"], "payments")
    load_dataframe_to_bigquery(data["reviews"], "reviews")