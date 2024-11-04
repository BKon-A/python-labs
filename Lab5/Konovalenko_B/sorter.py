import string
import re

def sorted_words(words):
    ua_words = sorted([word for word in words if word[0].lower() >= 'а' and word[0].lower() <= 'я'])
    en_words = sorted([word for word in words if word[0].lower() < 'а' or word[0].lower() > 'я'])
    return ua_words + en_words

def main():
    try:
        with open('text.txt', 'r', encoding='utf-8') as file:

            content = file.read()

            print("Вміст файлу:")
            print(content)

            sentences = re.split(r'[.!?]', content)

            first_sentence = next((s.strip() for s in sentences if s.strip()), None)
            if first_sentence:
                print(f"\nПерше речення: {first_sentence}")

                words = [word.strip(string.punctuation) for word in first_sentence.split()]
                print("Всі слова, відсортовані по алфавіту:")
                sorted_words_list = sorted_words(words)
                print(sorted_words_list)

                print(f"Кількість слів у першому реченні: {len(sorted_words_list)}")
            else:
                print("Не вдалося знайти речення.")

            all_words = re.findall(r'\b\w+\b', content)
            print(f"\nКількість слів у файлі: {len(all_words)}")

    except FileNotFoundError:
        print("Помилка: файл не знайдено.")
    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()
