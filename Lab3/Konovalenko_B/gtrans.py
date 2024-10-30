from translator import gtrans_module

def main():
    text = "Добрий день"
    
    # Визначення мови тексту
    lang = gtrans_module.LangDetect(text, "all")
    print(f"Detected Language Response: {lang}")
    if lang is None:
        print("Error: LangDetect returned None")
    elif isinstance(lang, str):
        print(f"Detected Language: {lang}")
    else:
        try:
            print(f"Detected Language: {lang.split(',')[0].split(': ')[1]}, Confidence: {lang.split(',')[1].split(': ')[1]}")
        except Exception as e:
            print(f"Error with LangDetect format: {e}")

    # Переклад тексту на англійську
    translated_text = gtrans_module.Translate(text, src="uk", dest="en")
    if translated_text is None:
        print("Error: Translate returned None")
    else:
        print(f"Translated Text: {translated_text}")

    # Отримання коду мови
    lang_code = gtrans_module.CodeLang("Ukrainian")
    if lang_code is None:
        print("Error: CodeLang returned None")
    else:
        print(f"Language Code for Ukrainian: {lang_code}")

    # Виведення списку всіх мов і перекладу тексту на екран
    print("Supported Languages (first 10):")
    result = gtrans_module.LanguageList("screen", text, limit=10)
    if result is None:
        print("Error: LanguageList returned None")
    else:
        print(result)

if __name__ == "__main__":
    main()
