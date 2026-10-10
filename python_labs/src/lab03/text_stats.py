import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.text import normalize, tokenize, count_freq, top_n

TABLE_MODE = True


def table(top: list[tuple[str, int]]) -> None:
    '''Печатает топ слов в виде выровненной таблицы

    Args:
        top: Список пар (слово, количество повторений), 
            например результат функции top_n

    Returns:
        None: Функция ничего не возвращает, только печатает таблицу.
            Ширина первого столбца равна длине самого длинного слова,
            но не меньше длины заголовка "слово".
    '''
    width = len("слово")
    for word, count in top_n:
        width = max(width, len(word))
    print("слово".ljust(width) + " | частота")
    print("-" * (width + 3 + len("частота")))
    for word, count in top_n:
        print(word.ljust(width) + " | " + str(count))


def main() -> None:
    '''Читает текст из stdin и печатает статистику по словам

    Весь ввод читается до EOF. Текст нормализуется, разбивается на слова,
    после чего печатаются общее число слов, число уникальных слов и топ-5.
    Формат топа зависит от константы TABLE_MODE: таблица (True)
    или строки вида "слово:кол-во" (False).

    Returns:
        None: Функция ничего не возвращает, только печатает результат.
    '''
    text = sys.stdin.read()
    new = normalize(text)
    words = tokenize(new)
    counter = count_freq(words)
    top = top_n(counter, 5)

    print(f"Всего слов: {len(words)}")
    print(f"Уникальных слов: {len(counter)}")
    print("Топ-5:")

    if TABLE_MODE:
        table(top)
    else:
        for word, count in top:
            print(f"{word}:{count}")


if __name__ == "__main__":
    main()