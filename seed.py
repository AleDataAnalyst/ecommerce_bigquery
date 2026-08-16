import argparse
from src.config import get_bigquery_client, DATASET_ID
from src.create_tables import create_dataset, create_tables
from src.generate_data import generate_synthetic_data
from src.load_data import load_dataframe_to_bigquery

def run_seed():
    print("🚀 Iniciando proceso de seeding (creación y carga de datos en BigQuery)...")
    
    # 1. Crear dataset y tablas
    print("\n--- PASO 1: Creando esquema en BigQuery ---")
    create_dataset()
    create_tables()
    
    # 2. Generar datos sintéticos
    print("\n--- PASO 2: Generando datos sintéticos con Faker ---")
    data = generate_synthetic_data()
    
    # 3. Cargar datos en BigQuery
    print("\n--- PASO 3: Subiendo datos a BigQuery ---")
    load_dataframe_to_bigquery(data["categories"], "categories")
    load_dataframe_to_bigquery(data["products"], "products")
    load_dataframe_to_bigquery(data["customers"], "customers")
    load_dataframe_to_bigquery(data["orders"], "orders")
    load_dataframe_to_bigquery(data["order_items"], "order_items")
    load_dataframe_to_bigquery(data["payments"], "payments")
    load_dataframe_to_bigquery(data["reviews"], "reviews")
    
    print("\n✨ ¡Proceso completado con éxito! Base de datos poblada y lista para consultas.")

if __name__ == "__main__":
    run_seed()