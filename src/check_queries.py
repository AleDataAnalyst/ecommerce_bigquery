from google.cloud import bigquery
from config import get_bigquery_client, DATASET_ID


def run_query_checks():
    client = get_bigquery_client()
    prefix = f"{client.project}.{DATASET_ID}"

    # Diccionario con las consultas clave para verificar el volumen y negocio
    queries = {
        "1. Total de Clientes (Esperado: 500)": f"SELECT COUNT(*) AS total FROM `{prefix}.customers`",
        "2. Total de Productos (Esperado: 70)": f"SELECT COUNT(*) AS total FROM `{prefix}.products`",
        "3. Total de Pedidos (Esperado: 2000)": f"SELECT COUNT(*) AS total FROM `{prefix}.orders`",
        "4. Total de Líneas de Pedido (Esperado: ~4569)": f"SELECT COUNT(*) AS total FROM `{prefix}.order_items`",
        "5. Total de Pagos (Esperado: 2000)": f"SELECT COUNT(*) AS total FROM `{prefix}.payments`",
        "6. Total de Reseñas": f"SELECT COUNT(*) AS total FROM `{prefix}.reviews`"
    }

    print("🔍 Ejecutando verificación de volúmenes y consultas en BigQuery...\n")
    for title, query in queries.items():
        print(f"--- {title} ---")
        df = client.query(query).to_dataframe()
        print(df.to_string(index=False))
        print("\n")


if __name__ == "__main__":
    run_query_checks()
