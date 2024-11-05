import os
import psycopg2
from prettytable import PrettyTable

# Параметри підключення до бази даних з environment
connection_params = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "db",
    "port": "5432"
}

def execute_query(query, params=None):
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Помилка виконання запиту: {e}")
        return None
    finally:
        if conn:
            conn.close()

def display_table(headers, rows):
    table = PrettyTable()
    table.field_names = headers
    for row in rows:
        table.add_row(row)
    print(table)

def get_ships_by_type(ship_type):
    query = """
    SELECT * FROM ships
    WHERE ship_type = %s;
    """
    result = execute_query(query, (ship_type,))
    if result:
        display_table(["Registration Number", "Name", "Captain Name", "Ship Type", "Capacity", "Year Built"], result)

def calculate_product_cost_per_batch():
    query = """
    SELECT b.batch_name, p.product_name, p.unit_price * b.quantity AS total_cost
    FROM batches b
    JOIN products p ON b.product_code = p.product_code;
    """
    result = execute_query(query)
    if result:
        display_table(["Batch Name", "Product Name", "Total Cost"], result)

def calculate_total_cost_per_batch():
    query = """
    SELECT b.batch_name, SUM(p.unit_price * b.quantity) AS total_batch_cost
    FROM batches b
    JOIN products p ON b.product_code = p.product_code
    GROUP BY b.batch_name;
    """
    result = execute_query(query)
    if result:
        display_table(["Batch Name", "Total Batch Cost"], result)

def count_product_types_in_batches():
    query = """
    SELECT b.batch_name, p.product_type, COUNT(*) AS product_count
    FROM batches b
    JOIN products p ON b.product_code = p.product_code
    GROUP BY b.batch_name, p.product_type;
    """
    result = execute_query(query)
    if result:
        display_table(["Batch Name", "Product Type", "Product Count"], result)

def calculate_arrival_date_for_batches():
    query = """
    SELECT b.batch_name, 
           (CURRENT_DATE + s.delivery_days) AS arrival_date
    FROM batches b
    JOIN shipment s ON b.batch_number = s.batch_number;
    """
    result = execute_query(query)
    if result:
        display_table(["Batch Name", "Arrival Date"], result)

def get_home_appliances():
    query = """
    SELECT * FROM products
    WHERE product_type = 'побутова техніка'
    ORDER BY product_name;
    """
    result = execute_query(query)
    if result:
        display_table(["Product Code", "Product Name", "Product Type", "Unit", "Unit Price", "Requires Custom Declaration"], result)

if __name__ == "__main__":
    # Приклад виконання запитів
    print("Судна за типом 'танкер':")
    get_ships_by_type('танкер')
    
    print("\nВартість кожного товару в кожній партії:")
    calculate_product_cost_per_batch()
    
    print("\nВартість кожної партії товарів:")
    calculate_total_cost_per_batch()
    
    print("\nКількість кожного типу товарів в кожній партії:")
    count_product_types_in_batches()
    
    print("\nДата прибуття в порт призначення для кожної партії товарів:")
    calculate_arrival_date_for_batches()
    
    print("\nВсі товари, які належать до типу 'побутова техніка':")
    get_home_appliances()
