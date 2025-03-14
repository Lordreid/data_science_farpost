"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""
from typing import List, Tuple
import string

file_path = "C:\\Users\\Lordreid\\Documents\\data_science_farpost\\11.03\\data.txt"

def read_and_decode_file(file_path: str) -> str:
    """Читает файл и обрабатывает специальные символы"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    encoded_content = content.encode()
    decoded_content = encoded_content.decode("unicode_escape")
    return decoded_content

def get_longest_diverse_words(text: str) -> List[str]:
    """Находит 10 самых длинных слов с наибольшим количеством уникальных букв"""
    words = text.split()
    clean_words = []
    
    for word in words:
        cleaned_word = word.strip(string.punctuation) # Очищаем слова от знаков препинания
        if cleaned_word:  # Пропускаем пустые строки
            clean_words.append(cleaned_word)
    
    word_features = []
    for word in clean_words:
        unique_chars = len(set(word))
        word_length = len(word)
        word_features.append((unique_chars, word_length, word))
    
    word_features.sort(reverse=True)
    
    result = []
    for i in range(min(10, len(word_features))):
        result.append(word_features[i][2])
    
    return result

def get_rarest_char(text: str) -> str:
    """Находит самый редкий символ в тексте"""
    char_counter = {}
    
    for char in text:
        if char in char_counter:
            char_counter[char] += 1
        else:
            char_counter[char] = 1
    
    min_count = float('inf')
    rarest_char = ''
    for char, count in char_counter.items():
        if count < min_count:
            min_count = count
            rarest_char = char
    return rarest_char

def count_punctuation_chars(text: str) -> int:
    """Считает все знаки препинания в тексте"""
    count = 0
    for char in text:
        if char in string.punctuation:
            count += 1
    return count

def count_non_ascii_chars(text: str) -> int:
    """Считает символы, выходящие за рамки стандартной ASCII таблицы"""
    count = 0
    for char in text:
        if ord(char) > 127:
            count += 1
    return count

def get_most_common_non_ascii_char(text: str) -> Tuple[str, int]:
    """Находит самый частый не-ASCII символ и количество его повторений"""
    non_ascii_counter = {}
    
    for char in text: # Собираем только не-ASCII символы
        if ord(char) > 127:
            if char in non_ascii_counter:
                non_ascii_counter[char] += 1
            else:
                non_ascii_counter[char] = 1
    
    if not non_ascii_counter:
        return ("Не найдено", 0)
    
    max_count = 0
    most_common_char = ''
    for char, count in non_ascii_counter.items():
        if count > max_count:
            max_count = count
            most_common_char = char
    return (most_common_char, max_count)

decoded_text = read_and_decode_file(file_path)

print("10 самых длинных слов с уникальными буквами:")
print(", ".join(get_longest_diverse_words(decoded_text)))

print("\nСамый редкий символ:", get_rarest_char(decoded_text))

print("\nКоличество знаков препинания:", count_punctuation_chars(decoded_text))

print("\nКоличество не-ASCII символов:", count_non_ascii_chars(decoded_text))

char, count = get_most_common_non_ascii_char(decoded_text)
print(f"\nСамый частый не-ASCII символ: '{char}' (встречается {count} раз)")