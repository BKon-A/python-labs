# Variant 14

import calculation_module

DATA_FILE = 'my_data.txt'

def read_data_from_file(filename):

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if len(lines) < 3:
                return None
            language = lines[0].strip()
            x = float(lines[1].strip())
            y = float(lines[2].strip())
            return language, x, y
    except (FileNotFoundError, ValueError):
        return None

def write_data_to_file(filename, language, x, y):
    
    with open(filename, 'w') as file:
        file.write(f"{language}\n{x}\n{y}\n")

def main():
    
    language = input("Введіть мову інтерфейсу (uk/en): ").strip().lower()
    if language not in ['uk', 'en']:
        print("Некоректна мова. Використано мову за замовчуванням: українська.")
        language = 'uk'
    
    data = read_data_from_file(DATA_FILE)
    
    if data:
        
        _, x, y = data
        print(f"{calculation_module.translate_text('Language', language)}: {language}")
        print(f"{calculation_module.translate_text('Two numbers x, y', language)}: {x} {y}")
        print(calculation_module.compare_squares(x, y, language))
    else:
        
        print(calculation_module.translate_text("Invalid data in file. Enter new values.", language))
        x, y = map(float, input(calculation_module.translate_text("Enter two numbers x, y", language) + ": ").split())
        write_data_to_file(DATA_FILE, language, x, y)
        print(f"{calculation_module.translate_text('Data saved to file', language)} [{DATA_FILE}]")

if __name__ == "__main__":
    main()