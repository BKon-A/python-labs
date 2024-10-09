def compare_squares(x, y, language):

    abs_diff_squares = abs(x**2 - y**2)
    square_diff = (x - y) ** 2

    result = translate_text(f"Module difference of squares |{x}^2 - {y}^2| = {abs_diff_squares}", language) + "\n"
    result += translate_text(f"Square difference ({x} - {y})^2 = {square_diff}", language) + "\n"
    
    if abs_diff_squares > square_diff:
        result += translate_text("Module difference is greater!", language)
    else:
        result += translate_text("Square difference is greater or equal!", language)
        
    return result

def translate_text(text, language):

    translations = {
        'uk': {
            'Enter two numbers x, y': 'Введіть два числа x, y',
            'Enter interface language': 'Введіть мову інтерфейсу',
            'Data saved to file': 'Дані збережено в файл',
            'Language': 'Мова',
            'Two numbers x, y': 'Два числа x, y',
            'Invalid data in file. Enter new values.': 'Некоректні дані у файлі. Введіть нові значення.',
            'Module difference is greater!': 'Модуль різності більше!',
            'Square difference is greater or equal!': 'Квадрат різності більше або дорівнює!',
            'Module difference of squares |': 'Модуль різності квадратів |',
            'Square difference (': 'Квадрат різності (',
            'greater!': 'більше!',
            'greater or equal!': 'більше або дорівнює!'
        },
        'en': {
            'Enter two numbers x, y': 'Enter two numbers x, y',
            'Enter interface language': 'Enter interface language',
            'Data saved to file': 'Data saved to file',
            'Language': 'Language',
            'Two numbers x, y': 'Two numbers x, y',
            'Invalid data in file. Enter new values.': 'Invalid data in file. Enter new values.',
            'Module difference is greater!': 'Module difference is greater!',
            'Square difference is greater or equal!': 'Square difference is greater or equal!',
            'Module difference of squares |': 'Module difference of squares |',
            'Square difference (': 'Square difference (',
            'greater!': 'greater!',
            'greater or equal!': 'greater or equal!'
        }
    }

    # print(f"Translating text: '{text}' for language: '{language}'")

    return translations.get(language, translations['uk']).get(text, text)
