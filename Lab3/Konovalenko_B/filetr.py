import json
import os
from translator import dtrans_module  # Або gtrans_module

def get_text_statistics(text: str):
    char_count = len(text)
    word_count = len(text.split())
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    return char_count, word_count, sentence_count

def read_text_with_limits(file_path: str, max_chars: int, max_words: int, max_sentences: int):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = ""
            char_count, word_count, sentence_count = 0, 0, 0
            
            for line in file:
                if char_count >= max_chars or word_count >= max_words or sentence_count >= max_sentences:
                    break
                
                text += line
                char_count, word_count, sentence_count = get_text_statistics(text)
            
            return text, char_count, word_count, sentence_count
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None, 0, 0, 0
    except Exception as e:
        print(f"Error reading the file: {str(e)}")
        return None, 0, 0, 0

def translate_file(config_path: str):
    # Читаємо конфігураційний файл
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Configuration file '{config_path}' not found.")
        return
    except json.JSONDecodeError:
        print("Error decoding the configuration file.")
        return
    
    text_file = config.get('text_file')
    target_language = config.get('target_language')
    output = config.get('output')
    max_chars = config['limits'].get('max_chars', 600)
    max_words = config['limits'].get('max_words', 100)
    max_sentences = config['limits'].get('max_sentences', 100)

    # Виводимо інформацію про текстовий файл якщо він існує
    if not os.path.exists(text_file):
        print(f"File '{text_file}' not found.")
        return

    print(f"File Name: {text_file}")
    file_size = os.path.getsize(text_file)
    print(f"File Size: {file_size} bytes")

    # Читаємо текстовий файл з лімітами
    text, char_count, word_count, sentence_count = read_text_with_limits(text_file, max_chars, max_words, max_sentences)
    
    if text is None:
        return

    print(f"Characters in file: {char_count}")
    print(f"Words in file: {word_count}")
    print(f"Sentences in file: {sentence_count}")

    # Визначаємо мову тексту
    detected_language = dtrans_module.LangDetect(text, 'lang')
    print(f"Detected Language: {detected_language}")

    # Перекладаємо текст
    try:
        translated_text = dtrans_module.Translate(text, src=detected_language, dest=target_language)
    except Exception as e:
        print(f"Error translating the text: {str(e)}")
        return

    # Виведення результату
    if output == 'screen':
        print(f"Translated Text to '{target_language}':\n{translated_text}")
    elif output == 'file':
        output_file = f"{os.path.splitext(text_file)[0]}_{target_language}.txt"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_text)
            print("Ok")
        except Exception as e:
            print(f"Error writing to file: {str(e)}")
    else:
        print("Invalid output option specified in the configuration.")

if __name__ == "__main__":
    translate_file("text_translate_conf.json")
