Отчет по лабораторной работе №3 — Тексты и частоты слов

Задание A — Библиотечный модуль src/lib/text.py

Реализован переиспользуемый модуль src/lib/text.py, содержащий функции для нормализации текста, токенизации, подсчета частоты слов и формирования топа слов.

1. Функция normalize

Преобразует строку: приведение к нижнему регистру (casefold), замена ё/Ё на е/Е и удаление управляющих символов и лишних пробелов.



<img width="575" height="527" alt="Снимок экрана — 2026-10-10 в 16 53 28" src="https://github.com/user-attachments/assets/863dcff7-7533-4b86-8065-1236c59c6f88" />




<img width="359" height="108" alt="Снимок экрана — 2026-10-10 в 16 49 52" src="https://github.com/user-attachments/assets/813179c0-7a39-444a-bc14-1a21e6308a15" /> 


Рис. 1. Результат работы и тестов функции normalize




2. Функция tokenize

Разбивает текст на слова (буквы, цифры, знак подчеркивания) по разделителям, сохраняя дефисы внутри слов.


<img width="280" height="59" alt="Снимок экрана — 2026-10-10 в 16 55 31" src="https://github.com/user-attachments/assets/f3dcecf4-310a-4aa7-97ba-99f784191f65" />


<img width="394" height="127" alt="Снимок экрана — 2026-10-10 в 16 50 01" src="https://github.com/user-attachments/assets/619b1514-c527-4686-8976-b456607d02d0" />


Рис. 2. Результат работы и тестов функции tokenize


3. Функции count_freq и top_n

count_freq подсчитывает частоту встречаемости токенов. 
top_n возвращает первые N частых слов с алфавитной сортировкой при равенстве частот.



<img width="621" height="517" alt="Снимок экрана — 2026-10-10 в 16 59 31" src="https://github.com/user-attachments/assets/771574ce-65ec-4956-8f17-8011adb1036d" />



<img width="632" height="126" alt="Снимок экрана — 2026-10-10 в 17 00 25" src="https://github.com/user-attachments/assets/729e4053-c545-45a3-bb0c-5246a2f8b077" />

Рис. 3. Результат работы и тестов функций count_freq и top_n




Задание B — Скрипт статистики src/lab03/text_stats.py

Скрипт читает вход из stdin, вызывает функции из src/lib/text.py и печатает базовую статистику текста.

Исходный код src/lab03/text_stats.py

```python
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
    for word, count in top:
        width = max(width, len(word))
    print("слово".ljust(width) + " | частота")
    print("-" * (width + 3 + len("частота")))
    for word, count in top:
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
```

Примеры работы:
Обычный режим вывода


<img width="309" height="101" alt="Снимок экрана — 2026-10-10 в 18 17 15" src="https://github.com/user-attachments/assets/008d5680-0b96-4818-838d-1c8b220f208a" />


Табличный режим вывода:

<img width="190" height="125" alt="Снимок экрана — 2026-10-10 в 18 19 47" src="https://github.com/user-attachments/assets/fb940c76-7b30-4764-9b39-2028bc83dc33" />
