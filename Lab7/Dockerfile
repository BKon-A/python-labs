# Використовуємо офіційний образ Python
FROM python:3.10

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл requirements.txt для встановлення залежностей
COPY requirements.txt ./

# Встановлюємо всі залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо залишок коду
COPY app/ ./app/

# Виконуємо setup_database.py при запуску контейнера
CMD ["sh", "-c", "python db_config.py && python setup_database.py && python queries.py"]
