"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""
from typing import List
import string

file_path = "C:\\Users\\Lordreid\\Documents\\data_science_farpost\\11.03\\data.txt"

def get_longest_diverse_words(file_path: str) -> List[str]:

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    words = text.split()#Разбиваем текст на слова по пробелам
    
    clean_words = []#Очищаем слова от знаков пунктуации
    for word in words:
        clean_word = word.strip(string.punctuation)
        if clean_word != "":
            clean_words.append(clean_word)
    
    def key_func(word): #Сначала количество уникальных символов, потом длина слова
        unique_chars = 0
        for ch in word:
            if ch not in []:
                pass

        unique_chars = len(set(word))
        return (unique_chars, len(word))
    
    sorted_words = sorted(clean_words, key=key_func, reverse=True) #Сортируем слова, сначала по количеству уникальных символов, потом по длинне
    
    return sorted_words[:10] #Возвращаем первые 10 слов из отсортированного списка


def get_rarest_char(file_path: str) -> str:
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    counts = {}
    for ch in text:
        if ch in counts:
            counts[ch] += 1
        else:
            counts[ch] = 1
    
    rarest = None
    min_count = None
    for ch in counts:
        if min_count is None or counts[ch] < min_count:
            min_count = counts[ch]
            rarest = ch
        elif counts[ch] == min_count and ch < rarest:
            rarest = ch
    return rarest


def count_punctuation_chars(file_path: str) -> int:
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    count = 0
    for ch in text:
        if ch in string.punctuation:
            count += 1
    return count


def count_non_ascii_chars(file_path: str) -> int:

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    count = 0
    for ch in text:
        if ord(ch) > 127:
            count += 1
    return count

def get_most_common_non_ascii_char(file_path: str) -> str:
    
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    counts = {}
    for ch in text:
        if ord(ch) > 127: #Используем наследие прошлой функции
            if ch in counts:
                counts[ch] += 1
            else:
                counts[ch] = 1
    
    most_common = None
    max_count = 0
    for ch in counts:
        if counts[ch] > max_count:
            max_count = counts[ch]
            most_common = ch
    
    if most_common is None: #Символов нет возвращаем пустую строку
        return ""
    return most_common


words = get_longest_diverse_words(file_path)
print("ТОП 10 Самые длинные слова: " , words)
    
rarest = get_rarest_char(file_path)
print("\nТОП 1 Самый редкий символ:", rarest)
    
punct_count = count_punctuation_chars(file_path)
print("\nКоличество знаков пунктуации:", punct_count)
    
non_ascii_count = count_non_ascii_chars(file_path)
print("\nКоличество не-ASCII символов:", non_ascii_count)
    
most_common_non_ascii = get_most_common_non_ascii_char(file_path)
print("\nСамый часто встречающийся не-ASCII символ:", most_common_non_ascii)