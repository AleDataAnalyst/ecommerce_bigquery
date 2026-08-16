from google.cloud import bigquery
from src.config import get_bigquery_client, DATASET_ID


def run_analytical_queries():
    client = get_bigquery_client()
    prefix = f"{client.project}.{DATASET_ID}"

    queries = {
        "1. Ingresos totales y pedidos por país de cliente": f"""
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

        "2. Top 5 productos más vendidos (unidades)": f"""
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

        "3. Rendimiento y margen por categoría de producto": f"""
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

        "4. Distribución de pedidos por estado": f"""
            SELECT 
                status,
                COUNT(order_id) AS order_count
            FROM `{prefix}.orders`
            GROUP BY status
            ORDER BY order_count DESC;
        """,

        "5. Valoración media por categoría de producto": f"""
            SELECT 
                cat.name AS category_name,
                ROUND(AVG(r.rating), 2) AS avg_rating,
                COUNT(r.review_id) AS total_reviews
            FROM `{prefix}.reviews` r
            JOIN `{prefix}.order_items` oi ON r.order_item_id = oi.order_item_id
            JOIN `{prefix}.products` pr ON oi.product_id = pr.product_id
            JOIN `{prefix}.categories` cat ON pr.category_id = cat.category_id
            GROUP BY cat.name
            ORDER BY avg_rating DESC;
        """
    }

    print("📊 Ejecutando queries analíticas de verificación en BigQuery...\n")
    for title, query in queries.items():
        print(f"================ {title} ================")
        df = client.query(query).to_dataframe()
        print(df.to_string(index=False))
        print("\n")


if __name__ == "__main__":
    run_analytical_queries()
