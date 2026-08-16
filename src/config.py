import os
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

# Cargar las variables de entorno desde el fichero .env
load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def get_bigquery_client():
    """
    Inicializa y devuelve un cliente de Google BigQuery 
    utilizando las credenciales del Service Account configuradas en el .env.
    """
    if not CREDENTIALS_PATH or not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"No se ha encontrado el archivo de credenciales en la ruta: {CREDENTIALS_PATH}. "
            "Asegúrate de colocar tu JSON en la carpeta credentials/ y configurar el .env."
        )

    # Cargar credenciales explícitamente desde el JSON
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH)

    # Crear cliente de BigQuery
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    return client


if __name__ == "__main__":
    # Test rápido de conexión
    try:
        client = get_bigquery_client()
        print(
            f"✅ Conexión a BigQuery establecida con éxito para el proyecto: {PROJECT_ID}")
    except Exception as e:
        print(f"❌ Error al conectar con BigQuery: {e}")
