import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

# Inicializar Faker (puedes usar locale de España o internacional, usaremos es_ES por variedad)
fake = Faker("es_ES")

def generate_synthetic_data():
    print("🔄 Generando datos sintéticos...")

    # 1. Categories (5 categorías de tecnología)
    categories_data = [
        {"category_id": 1, "name": "Smartphones", "description": "Teléfonos inteligentes y accesorios"},
        {"category_id": 2, "name": "Laptops", "description": "Ordenadores portátiles y equipos de trabajo"},
        {"category_id": 3, "name": "Audio", "description": "Auriculares, altavoces y sistemas de sonido"},
        {"category_id": 4, "name": "Wearables", "description": "Relojes inteligentes y pulseras de actividad"},
        {"category_id": 5, "name": "Periféricos", "description": "Teclados, ratones y monitores"}
    ]
    df_categories = pd.DataFrame(categories_data)

    # 2. Products (70 productos)
    products_data = []
    for i in range(1, 71):
        cost = round(random.uniform(20.0, 800.0), 2)
        margin = random.uniform(1.2, 1.8) # Margen de beneficio
        price = round(cost * margin, 2)
        products_data.append({
            "product_id": i,
            "category_id": random.randint(1, 5),
            "name": f"{fake.word().capitalize()} {fake.word().capitalize()} {i}",
            "price": price,
            "cost": cost,
            "stock": random.randint(10, 200),
            "is_active": True
        })
    df_products = pd.DataFrame(products_data)

    # 3. Customers (500 clientes)
    channels = ["organic", "paid_ads", "social_media", "email_marketing", "affiliates"]
    countries = ["España", "Francia", "Alemania", "Italia", "Portugal"]
    customers_data = []
    for i in range(1, 501):
        reg_date = fake.date_between(start_date="-2y", end_date="today")
        customers_data.append({
            "customer_id": i,
            "name": fake.name(),
            "country": random.choice(countries),
            "city": fake.city(),
            "acquisition_channel": random.choice(channels),
            "registration_date": reg_date
        })
    df_customers = pd.DataFrame(customers_data)

    # 4. Orders (2000 pedidos) & 5. Order Items (~4500 líneas) & 6. Payments
    orders_data = []
    order_items_data = []
    payments_data = []
    
    statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled", "returned"]
    payment_methods = ["credit_card", "paypal", "bizum", "bank_transfer"]
    payment_statuses = ["completed", "refunded", "pending", "failed"]

    item_id_counter = 1
    payment_id_counter = 1

    for order_id in range(1, 2001):
        customer_id = random.randint(1, 500)
        status = random.choices(statuses, weights=[10, 15, 20, 45, 5, 5], k=1)[0]
        
        # Generar fechas coherentes
        order_date = fake.date_time_between(start_date="-1y", end_date="now")
        shipping_date = order_date + timedelta(days=random.randint(1, 3)) if status in ["shipped", "delivered", "returned"] else None
        delivery_date = shipping_date + timedelta(days=random.randint(1, 4)) if status == "delivered" else None

        orders_data.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "status": status,
            "order_date": order_date,
            "shipping_date": shipping_date,
            "delivery_date": delivery_date
        })

        # Líneas de pedido (2 a 3 productos por pedido de media)
        num_items = random.choices([1, 2, 3, 4], weights=[20, 45, 25, 10], k=1)[0]
        chosen_products = random.sample(list(df_products["product_id"]), num_items)
        
        order_total_amount = 0
        for prod_id in chosen_products:
            prod_row = df_products[df_products["product_id"] == prod_id].iloc[0]
            quantity = random.randint(1, 3)
            unit_price = prod_row["price"]
            discount = round(random.choice([0.0, 0.0, 0.0, 0.05, 0.10, 0.15]), 2)
            
            subtotal = (unit_price * quantity) * (1 - discount)
            order_total_amount += subtotal

            order_items_data.append({
                "order_item_id": item_id_counter,
                "order_id": order_id,
                "product_id": prod_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount
            })
            item_id_counter += 1

        # Pago asociado al pedido
        p_status = "completed" if status not in ["cancelled", "pending"] else random.choice(payment_statuses)
        payments_data.append({
            "payment_id": payment_id_counter,
            "order_id": order_id,
            "payment_method": random.choice(payment_methods),
            "status": p_status,
            "amount": round(order_total_amount, 2),
            "payment_date": order_date
        })
        payment_id_counter += 1

    df_orders = pd.DataFrame(orders_data)
    df_order_items = pd.DataFrame(order_items_data)
    df_payments = pd.DataFrame(payments_data)

    # 7. Reviews (~35% de los productos de pedidos entregados)
    delivered_order_items = df_order_items.merge(
        df_orders[df_orders["status"] == "delivered"], on="order_id"
    )
    
    reviews_data = []
    review_id_counter = 1
    for _, row in delivered_order_items.iterrows():
        if random.random() < 0.35:  # ~35 de probabilidad
            reviews_data.append({
                "review_id": review_id_counter,
                "order_item_id": row["order_item_id"],
                "rating": random.choices([1, 2, 3, 4, 5], weights=[5, 5, 15, 35, 40], k=1)[0],
                "comment": fake.sentence() if random.random() > 0.3 else None
            })
            review_id_counter += 1

    df_reviews = pd.DataFrame(reviews_data)

    print("✅ ¡Datos sintéticos generados con éxito!")
    
    return {
        "categories": df_categories,
        "products": df_products,
        "customers": df_customers,
        "orders": df_orders,
        "order_items": df_order_items,
        "payments": df_payments,
        "reviews": df_reviews
    }

if __name__ == "__main__":
    data = generate_synthetic_data()
    for name, df in data.items():
        print(f" - Tabla '{name}': {len(df)} registros")