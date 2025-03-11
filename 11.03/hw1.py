"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""
from typing import List

file_path = "11.03\\data.txt"

def get_longest_diverse_words(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    words = text.split()
    # Sort by number of unique characters (descending), then by word length (descending)
    sorted_words = sorted(words, key=lambda x: (-len(set(x)), -len(x)))
    return sorted_words[:10]

'''
def get_rarest_char(file_path: str) -> str:
    ...


def count_punctuation_chars(file_path: str) -> int:
    ...


def count_non_ascii_chars(file_path: str) -> int:
    ...


def get_most_common_non_ascii_char(file_path: str) -> str:
    ...

'''

get_longest_diverse_words(file_path)