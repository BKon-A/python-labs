import os
from sqlalchemy import create_engine

# Читаємо параметри підключення з оточення
DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine():
    return create_engine(DATABASE_URL)
