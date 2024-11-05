import os
import psycopg2
from psycopg2 import sql

# Параметри підключення до бази даних з environment
connection_params = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "db",
    "port": "5432"
}

def create_database():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=connection_params['user'],
            password=connection_params['password'],
            host=connection_params['host'],
            port=connection_params['port']
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (connection_params['dbname'],))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(connection_params['dbname'])))
            print(f"База даних {connection_params['dbname']} була створена.")
        else:
            print(f"База даних {connection_params['dbname']} вже існує.")
        
        cursor.close()
    except Exception as e:
        print(f"Помилка при створенні бази даних: {e}")
    finally:
        if conn:
            conn.close()

def check_tables_exist(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        tables = cursor.fetchall()
        cursor.close()
        return {table[0] for table in tables}  # Повертаємо множину таблиць
    except Exception as e:
        print(f"Помилка при перевірці таблиць: {e}")
        return set()

def create_tables(conn):
    existing_tables = check_tables_exist(conn)
    
    commands = [
        """
        CREATE TABLE IF NOT EXISTS products (
            product_code SERIAL PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            product_type VARCHAR(50) CHECK (product_type IN ('пально-мастильні суміші', 'побутова техніка', 'великогабаритний вантаж')),
            unit VARCHAR(20) NOT NULL,
            unit_price NUMERIC(10, 2) CHECK (unit_price > 0),
            requires_custom_declaration BOOLEAN DEFAULT FALSE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ports (
            port_number SERIAL PRIMARY KEY,
            port_name VARCHAR(100) NOT NULL,
            country VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ships (
            registration_number SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            captain_name VARCHAR(100),
            ship_type VARCHAR(50) CHECK (ship_type IN ('танкер', 'суховантажний')),
            capacity INTEGER CHECK (capacity > 0),
            year_built INTEGER CHECK (year_built > 1900)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS batches (
            batch_number SERIAL PRIMARY KEY,
            batch_name VARCHAR(100),
            product_code INTEGER REFERENCES products(product_code) ON DELETE CASCADE,
            quantity INTEGER CHECK (quantity > 0),
            destination_port INTEGER REFERENCES ports(port_number) ON DELETE SET NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS shipment (
            shipment_code SERIAL PRIMARY KEY,
            batch_number INTEGER REFERENCES batches(batch_number) ON DELETE CASCADE,
            shipment_date DATE NOT NULL,
            delivery_days INTEGER CHECK (delivery_days >= 0),
            ship_number INTEGER REFERENCES ships(registration_number) ON DELETE SET NULL
        )
        """
    ]

    try:
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
            print(f"Таблиця {command.split()[5]} створена.")
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Помилка при створенні таблиць: {e}")

def insert_data(conn):
    data = {
        "products": [
            ("Fuel Oil", "пально-мастильні суміші", "liters", 1.2, True),
            ("TV", "побутова техніка", "units", 250.0, False),
            ("Crane", "великогабаритний вантаж", "units", 15000.0, True),
            ("Washing Machine", "побутова техніка", "units", 300.0, False),
            ("Diesel", "пально-мастильні суміші", "liters", 1.1, True),
            ("Refrigerator", "побутова техніка", "units", 400.0, False),
            ("Jet Fuel", "пально-мастильні суміші", "liters", 2.0, True),
            ("Dishwasher", "побутова техніка", "units", 350.0, False),
            ("Generator", "великогабаритний вантаж", "units", 12000.0, True),
            ("Laptop", "побутова техніка", "units", 900.0, False),
            ("Natural Gas", "пально-мастильні суміші", "cubic meters", 0.5, True),
            ("Coffee Maker", "побутова техніка", "units", 80.0, False),
            ("Solar Panels", "великогабаритний вантаж", "units", 5000.0, True),
            ("Microwave", "побутова техніка", "units", 100.0, False),
            ("Mobile Phone", "побутова техніка", "units", 700.0, False)
        ],
        "ports": [
            ("Odessa", "Ukraine"),
            ("Istanbul", "Turkey"),
            ("New York", "USA"),
            ("Rotterdam", "Netherlands"),
            ("Shanghai", "China")
        ],
        "ships": [
            ("Aurora", "Ivan Petrenko", "танкер", 15000, 2005),
            ("Phoenix", "Olegio Martini", "суховантажний", 10000, 2010),
            ("Sea Star", "Anna Lysenko", "танкер", 18000, 2012)
        ],
        "batches": [
            ("Batch 1", 1, 5000, 1),
            ("Batch 2", 2, 20, 3),
            ("Batch 3", 3, 3, 2),
            ("Batch 4", 4, 15, 4),
            ("Batch 5", 5, 10, 5)
        ],
        "shipment": [
            (1, "2024-11-10", 7, 1),
            (2, "2024-11-12", 5, 2),
            (3, "2024-11-15", 15, 3),
            (4, "2024-11-18", 10, 1),
            (5, "2024-11-20", 12, 2)
        ]
    }

    try:
        cursor = conn.cursor()

        # Вставка даних у таблицю products
        for row in data["products"]:
            insert_query = sql.SQL("INSERT INTO products (product_name, product_type, unit, unit_price, requires_custom_declaration) VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(insert_query, row)
        print("Дані успішно вставлені у таблицю products.")

        # Вставка даних у таблицю ports
        for row in data["ports"]:
            insert_query = sql.SQL("INSERT INTO ports (port_name, country) VALUES (%s, %s)")
            cursor.execute(insert_query, row)
        print("Дані успішно вставлені у таблицю ports.")

        # Вставка даних у таблицю ships
        for row in data["ships"]:
            insert_query = sql.SQL("INSERT INTO ships (name, captain_name, ship_type, capacity, year_built) VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(insert_query, row)
        print("Дані успішно вставлені у таблицю ships.")

        # Вставка даних у таблицю batches
        for row in data["batches"]:
            insert_query = sql.SQL("INSERT INTO batches (batch_name, product_code, quantity, destination_port) VALUES (%s, %s, %s, %s)")
            cursor.execute(insert_query, row)
        print("Дані успішно вставлені у таблицю batches.")

        # Вставка даних у таблицю shipment
        for row in data["shipment"]:
            insert_query = sql.SQL("INSERT INTO shipment (batch_number, shipment_date, delivery_days, ship_number) VALUES (%s, %s, %s, %s)")
            cursor.execute(insert_query, row)
        print("Дані успішно вставлені у таблицю shipment.")

        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Помилка при вставці даних: {e}")

if __name__ == "__main__":
    create_database()

    # Підключення до новоствореної бази даних
    try:
        conn = psycopg2.connect(
            dbname=connection_params['dbname'],
            user=connection_params['user'],
            password=connection_params['password'],
            host=connection_params['host'],
            port=connection_params['port']
        )

        create_tables(conn)
        insert_data(conn)
    except Exception as e:
        print(f"Помилка при підключенні до бази даних: {e}")
    finally:
        if conn:
            conn.close()
