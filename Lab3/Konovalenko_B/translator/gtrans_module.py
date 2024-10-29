from google.cloud import translate_v2;

googleTrans = translate_v2.Client()

LANGUAGES = googleTrans.get_languages()

def LangDetect(text: str, set: str = 'all') -> str:
    # Функція визначає мову та коефіцієнт довіри для заданого тексту, або повертає повідомлення про помилку.
    # text – текст для якого потрібно визначити мову та коефіцієнт довіри;
    # set = “lang” – функція повертає тільки мову тексту
    # set = “confidence” – функція повертає тільки коефіцієнт довіри
    # set = “all” (по замовченню) – функція повертає мову і коефіцієнт довіри

    try:
        detection = googleTrans.detect_language(text)
        
        if set == 'lang':
            return detection['language']
        elif set == 'confidence':
            return str(detection['confidence'])
        elif set == 'all':
            return f"Language: {detection['language']}, Confidence: {detection['confidence']}"
        else:
            return "Invalid 'set' parameter value."
    except Exception as e:
        return f"Error: {str(e)}"

def Translate(text: str, src: str = 'auto', dest: str = 'en') -> str:
    # Функція повертає текст перекладений на задану мову, або повідомлення про помилку.
    # text – текст, який необхідно перекласти;
    # src – назва або код мови заданого тексту, відповідно до стандарту ISO-639, або значення ‘auto’;
    # dest – назва або код мови на яку необхідно перевести заданий текст, відповідно до стандарту ISO-639

    try:
        translation = googleTrans.translate(text, source_language=src, target_language=dest)
        return translation['translatedText']
    except Exception as e:
        return f"Error: {str(e)}"

def CodeLang(lang: str) -> str:
    # Функція повертає код мови (відповідно до таблиці), якщо в параметрі lang міститься назва мови, або повертає
    # назву мови, якщо в параметрі lang міститься її код, або повідомлення про помилку
    # lang - назва мови або код мови

    try:
        if lang in LANGUAGES:
            return LANGUAGES[lang]
        else:
            for name, code in LANGUAGES.items():
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
        table = "N  Language        ISO-639 code        Text\n" + "-" * 56 + "\n"
        
        index = 1
     
        for lang in LANGUAGES:
            code = lang['language']
            name = lang['name']
        
            if index > limit:
                break

            translated_text = ""
            if text:
                try:

                    translation = googleTrans.translate(text, target_language=code)
                    translated_text = translation['translatedText']
                except Exception as e:
                    print(f"Error translating to {name} ({code}): {str(e)}")
                    translated_text = "Translation failed"

            table += f"{index:<3} {name:<15} {code:<10}\t  {translated_text}\n"
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