from deep_translator import GoogleTranslator;
from langdetect import detect;
from langdetect.lang_detect_exception import LangDetectException;
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES;
from deep_translator.exceptions import TranslationNotFound;

def LangDetect(text: str, mode: str = 'all') -> str:
    # Функція визначає мову та коефіцієнт довіри для заданого тексту, або повертає повідомлення про помилку.
    # text – текст для якого потрібно визначити мову та коефіцієнт довіри;
    # set = “lang” – функція повертає тільки мову тексту
    # set = “confidence” – функція повертає тільки коефіцієнт довіри
    # set = “all” (по замовченню) – функція повертає мову і коефіцієнт довіри

    try:
        detected_lang = detect(text)
        confidence = 0.99  # У langdetect немає коефіцієнта впевненості, тому використовується умовний

        if mode == "lang":
            return detected_lang
        elif mode == "confidence":
            return confidence
        else:
            return {"lang": detected_lang, "confidence": confidence}
    except Exception as e:
        return f"Error: {str(e)}"

def Translate(text: str, src: str = 'auto', dest: str = 'en') -> str:
    # Функція повертає текст перекладений на задану мову, або повідомлення про помилку.
    # text – текст, який необхідно перекласти;
    # src – назва або код мови заданого тексту, відповідно до стандарту ISO-639, або значення ‘auto’;
    # dest – назва або код мови на яку необхідно перевести заданий текст, відповідно до стандарту ISO-639

    try:
        translation = GoogleTranslator(source=src, target=dest)
        translated_text = translation.translate(text)
        return translated_text
    except Exception as e:
        return f"Error: {str(e)}"

def CodeLang(lang: str) -> str:
    # Функція повертає код мови (відповідно до таблиці), якщо в параметрі lang міститься назва мови, або повертає
    # назву мови, якщо в параметрі lang міститься її код, або повідомлення про помилку
    # lang - назва мови або код мови

    try:
        if lang in GOOGLE_LANGUAGES_TO_CODES:
            return GOOGLE_LANGUAGES_TO_CODES[lang]
        else:
            for name, code in GOOGLE_LANGUAGES_TO_CODES.items():
                if name.lower() == lang.lower():
                    return code
            return "Language not found."
    except Exception as e:
        return f"Error: {str(e)}"

def LanguageList(out: str = 'screen', text: str = None, limit: int = 10) -> str:
    # Виводить в файл або на екран таблицю всіх мов, що підтримуються, та їх кодів, 
    # а також текст, перекладений на цю мову. Повертає ‘Ok’, якщо всі операції виконані, або повідомлення про помилку. 
    # out = “screen” (по замовченню) – вивести таблицю на екран 
    # out = “file” – вивести таблицю в файл. (Тип файлу на розсуд студента)
    # text – текст, який необхідно перекласти. Якщо параметр відсутній, то відповідна колонка в таблиці також повинна бути відсутня.

    try:
        table = "N  Language        ISO-639 code    Text\n" + "-" * 56 + "\n"
        
        index = 1
        
        for code, name in GOOGLE_LANGUAGES_TO_CODES.items():
            if index > limit:
                break

            translated_text = ""
            if text:
                try:
                    translated_text = GoogleTranslator(source='auto', target=code).translate(text)
                except TranslationNotFound:
                    translated_text = "Translation failed"

            table += f"{index:<3} {name:<15}    {code:<8}\t{translated_text}\n"
            index += 1

        if out == 'screen':
            print(table)
        elif out == 'file':
            with open('language_list.txt', 'w', encoding='utf-8') as f:
                f.write(table)
        else:
            return "Invalid 'out' parameter value."

        return "Ok"
    except Exception as e:
        return f"Error: {str(e)}"