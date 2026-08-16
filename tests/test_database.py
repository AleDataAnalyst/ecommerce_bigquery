import unittest
from src.config import get_bigquery_client, DATASET_ID


class TestECommerceDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = get_bigquery_client()
        cls.dataset_id = DATASET_ID

    def test_tables_existence(self):
        """Verifica que todas las tablas del modelo 3NF existan en BigQuery."""
        tables = ["categories", "products", "customers",
                  "orders", "order_items", "payments", "reviews"]
        for table_name in tables:
            table_ref = f"{self.client.project}.{self.dataset_id}.{table_name}"
            try:
                self.client.get_table(table_ref)
            except Exception:
                self.fail(
                    f"La tabla requerida '{table_name}' no existe en BigQuery.")

    def test_no_orphan_orders(self):
        """Verifica la integridad lógica: no debe haber órdenes sin un cliente válido."""
        query = f"""
            SELECT count(*) as orphan_count 
            FROM `{self.client.project}.{self.dataset_id}.orders` o
            LEFT JOIN `{self.client.project}.{self.dataset_id}.customers` c ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL AND o.customer_id IS NOT NULL
        """
        result = list(self.client.query(query).result())[0]
        self.assertEqual(result.orphan_count, 0,
                         "Se detectaron órdenes huérfanas sin cliente asociado.")


if __name__ == "__main__":
    unittest.main()
