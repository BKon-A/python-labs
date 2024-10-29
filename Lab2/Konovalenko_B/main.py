from google.cloud import translate_v2 as translate

translate_client = translate.Client()

def Translate(text, target_language):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def LangDetect(text):
    result = translate_client.detect_language(text)
    language = result['language']
    confidence = result['confidence']
    return language, confidence
    

def CodeLang(lang):
    try:
        language_codes = {
            'en': 'English',
            'de': 'German',
            'fr': 'French',
            'es': 'Spanish',
            'uk': 'Ukrainian',
        }
        if lang in language_codes:
            return language_codes[lang]

        for code, name in language_codes.items():
            if lang.lower() == name.lower():
                return code
    except Exception as e:
        print(f"Unexpected error in CodeLang function: {e}")
    return None

def main():
    text = input("Enter text to translate: ")
    target_language = input("Enter target language (en, de, fr, es, uk or full language name): ")

    fromLang, confidence = LangDetect(text)
    if fromLang is None or confidence is None:
        print("Failed to detect language.")
        return

    print(f"Detected language: {fromLang} (confidence: {confidence})")

    if len(target_language) > 2:
        target_language = CodeLang(target_language)

    if target_language is None:
        print("Invalid language or code. Please try again.")
        return

    translated_text = Translate(text, target_language)
    if translated_text:
        print(f"Translated text ({fromLang} -> {target_language}): {translated_text}")
    else:
        print("Translation failed.")

if __name__ == "__main__":
    main()
