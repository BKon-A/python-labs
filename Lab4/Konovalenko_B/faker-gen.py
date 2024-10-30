from faker import Faker
import csv
import random
from datetime import date

# Ініціалізація Faker з українською локалізацією
faker = Faker('uk_UA')

# Словники для По батькові
middle_names_male = ["Іванович", "Петрович", "Сергійович", "Андрійович", "Олександрович", "Васильович", "Миколайович", "Дмитрович", "Володимирович", "Богданович",
                     "Тарасович", "Степанович", "Павлович", "Юрійович", "Ігорович", "Георгійович", "Артемович", "Романович", "Ярославович", "Вікторович"]
middle_names_female = ["Іванівна", "Петрівна", "Сергіївна", "Андріївна", "Олександрівна", "Василівна", "Миколаївна", "Дмитрівна", "Володимирівна", "Богданівна",
                       "Тарасівна", "Степанівна", "Павлівна", "Юріївна", "Ігорівна", "Георгіївна", "Артемівна", "Романівна", "Ярославівна", "Вікторівна"]

# Функція для вибору по батькові залежно від статі
def get_middle_name(gender):
    return random.choice(middle_names_female if gender == 'Female' else middle_names_male)

# Функція для форматування дати народження у форматі РРРР-ММ-ДД
def format_date_of_birth():
    birth_date = faker.date_of_birth(minimum_age=16, maximum_age=85)
    return birth_date.strftime("%Y-%m-%d")

# Генерація і запис даних
with open('employees.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["Прізвище", "Ім’я По-батькові", "Стать", "Дата народження", "Посада", "Місто", "Адреса", "Телефон", "Email"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for _ in range(2000):
        gender = "Female" if random.random() < 0.4 else "Male"
        first_name = faker.first_name_female() if gender == "Female" else faker.first_name_male()
        row = {
            "Прізвище": faker.last_name(),
            "Ім’я По-батькові": f"{first_name} {get_middle_name(gender)}",
            "Стать": "Жіноча" if gender == "Female" else "Чоловіча",
            "Дата народження": format_date_of_birth(),
            "Посада": faker.job(),
            "Місто": faker.city(),
            "Адреса": faker.address(),
            "Телефон": faker.phone_number(),
            "Email": faker.email()
        }
        writer.writerow(row)
