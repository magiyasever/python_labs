import re
import unicodedata
TOKEN_RE = re.compile(r"\w+(?:-\w+)*")

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    '''Нормализует текст

    Args:
        text: Исходный текст
        casefold: Bool значение
                    True: Переводит все буквы в строчные
                    False: Оставляет всё как есть
        yo2e: Заменяет ё/Ё на е/Е

    Returns:
        обработанный текст
    '''
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()

    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")
    
    result = []
    for char in text:
        if unicodedata.category(char) == "Cc":
            result.append(' ')
        else:
            result.append(char)
    new_text = ''.join(result)
    return ' '.join(new_text.split())

def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text)

def count_freq(tokens: list[str]) -> dict[str, int]:
    '''Считает количество повторений токенов

    Args:
        tokens: Список слов (токенов)

    Returns:
        freq: Словарь: [слово], [количество повторений]
    '''
    freq = {}
    for token in tokens:
        if token in freq:
            freq[token] += 1
        else:
            freq[token] = 1
    return freq

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    '''Выводит топ n слов по частоте обращения

    Args:
        freq: Словарь где указаны слова и кол-во их повторений
        n: Кол-во элементов которые нужно указать в топе

    Returns:  Список где находятся кортежи (слово, количество повторений)
    '''
    return sorted(freq.items(), key = lambda x: (-x[1], x[0]))[:n]


if __name__ == "__main__":


    print(fr'''
        normalize

        "ПрИвЕт\nМИр\t" -> {normalize("ПрИвЕт\nМИр\t")}
        "ёжик, Ёлка" -> {normalize("ёжик, Ёлка")}
        "Hello\r\nWorld" -> {normalize("Hello\r\nWorld")}
        "  двойные   пробелы  " -> {normalize("  двойные   пробелы  ")}
        ''')

    print(fr'''
        tokenize

        "привет мир" -> {tokenize("привет мир")}
        "hello,world!!!" -> {tokenize("hello,world!!!")}
        "по-настоящему круто" -> {tokenize("по-настоящему круто")}
        "2025 год" -> {tokenize("2025 год")}
        "emoji 😀 не слово" -> {tokenize("emoji 😀 не слово")}
        ''')

    print(fr'''
        count_freq + top_n

        Токены ["a","b","a","c","b","a"] -> частоты {count_freq(["a", "b", "a", "c", "b", "a"])};
        top_n(..., n=2) -> {top_n(count_freq(["a", "b", "a", "c", "b", "a"]), 2)}

        При равенстве частот: токены ["bb","aa","bb","aa","cc"] -> {count_freq(["bb", "aa", "bb", "aa", "cc"])};
        top_n(..., n=2) → {top_n(count_freq(["bb", "aa", "bb", "aa", "cc"]), 2)}
        ''')