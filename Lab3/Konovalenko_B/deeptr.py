from translator import dtrans_module

def main():
    text = "Добрий день"
    
    # Визначення мови та коефіцієнту впевненості
    lang = dtrans_module.LangDetect(text, "all")
    print(f"Detected Language: {lang['lang']}, Confidence: {lang['confidence']}")

    # Переклад тексту на англійську
    translated_text = dtrans_module.Translate(text, src="uk", dest="en")
    print(f"Translated Text: {translated_text}")

    # Отримання коду мови
    lang_code = dtrans_module.CodeLang("Ukrainian")
    print(f"Language Code for Ukrainian: {lang_code}")

    # Виведення списку всіх мов і перекладу тексту на екран
    print("Supported Languages:")
    result = dtrans_module.LanguageList("screen", text)
    print(result)

if __name__ == "__main__":
    main()
