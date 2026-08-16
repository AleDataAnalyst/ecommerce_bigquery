from google.cloud import bigquery
from src.config import get_bigquery_client, DATASET_ID

def run_analytical_queries():
    client = get_bigquery_client()
    prefix = f"{client.project}.{DATASET_ID}"

    queries = {
        "1. Ingresos totales y pedidos por país": f"""
            SELECT 
                c.country,
                COUNT(DISTINCT o.order_id) AS total_orders,
                ROUND(SUM(p.amount), 2) AS total_revenue
            FROM `{prefix}.orders` o
            JOIN `{prefix}.customers` c ON o.customer_id = c.customer_id
            JOIN `{prefix}.payments` p ON o.order_id = p.order_id
            WHERE p.status = 'completed'
            GROUP BY c.country
            ORDER BY total_revenue DESC;
        """,
        "2. Top 5 productos más vendidos": f"""
            SELECT 
                pr.name AS product_name,
                SUM(oi.quantity) AS total_units_sold,
                ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS product_revenue
            FROM `{prefix}.order_items` oi
            JOIN `{prefix}.products` pr ON oi.product_id = pr.product_id
            GROUP BY pr.name
            ORDER BY total_units_sold DESC
            LIMIT 5;
        """,
        "3. Rentabilidad por categoría": f"""
            SELECT 
                cat.name AS category_name,
                COUNT(oi.order_item_id) AS items_sold,
                ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_sales,
                ROUND(SUM(oi.quantity * pr.cost), 2) AS total_cost,
                ROUND(SUM(oi.quantity * oi.unit_price) - SUM(oi.quantity * pr.cost), 2) AS estimated_profit
            FROM `{prefix}.order_items` oi
            JOIN `{prefix}.products` pr ON oi.product_id = pr.product_id
            JOIN `{prefix}.categories` cat ON pr.category_id = cat.category_id
            GROUP BY cat.name
            ORDER BY estimated_profit DESC;
        """,
        "4. Métodos de pago preferidos": f"""
            SELECT 
                payment_method,
                COUNT(payment_id) AS usage_count,
                ROUND(AVG(amount), 2) AS avg_transaction_value
            FROM `{prefix}.payments`
            GROUP BY payment_method
            ORDER BY usage_count DESC;
        """,
        "5. Tasa de conversión por canal de adquisición": f"""
            SELECT 
                c.acquisition_channel,
                COUNT(DISTINCT c.customer_id) AS total_customers,
                COUNT(DISTINCT o.order_id) AS total_orders,
                ROUND(COUNT(DISTINCT o.order_id) / NULLIF(COUNT(DISTINCT c.customer_id), 0), 2) AS orders_per_customer
            FROM `{prefix}.customers` c
            LEFT JOIN `{prefix}.orders` o ON c.customer_id = o.customer_id
            GROUP BY c.acquisition_channel
            ORDER BY orders_per_customer DESC;
        """,
        "6. Clientes recurrentes (TOP 10)": f"""
            SELECT 
                c.name,
                COUNT(o.order_id) AS order_count,
                ROUND(SUM(p.amount), 2) AS total_spent
            FROM `{prefix}.customers` c
            JOIN `{prefix}.orders` o ON c.customer_id = o.customer_id
            JOIN `{prefix}.payments` p ON o.order_id = p.order_id
            WHERE p.status = 'completed'
            GROUP BY c.name
            HAVING order_count > 1
            ORDER BY total_spent DESC
            LIMIT 10;
        """
    }

    print("📊 Ejecutando queries analíticas en BigQuery...\n")
    for title, query in queries.items():
        print(f"================ {title} ================")
        df = client.query(query).to_dataframe()
        print(df.to_string(index=False))
        print("\n")

if __name__ == "__main__":
    run_analytical_queries()