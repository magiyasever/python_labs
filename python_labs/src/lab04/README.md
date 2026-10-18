Отчет по лабораторной работе №4 — Файлы: TXT/CSV и отчеты по текстовой статистике

Задание A — модуль ввода/вывода src/lab04/io_txt_csv.py

Реализован модуль для чтения текстовых файлов и записи результатов в CSV. Для работы с путями используется Path, а для формирования CSV — стандартный модуль csv.

1. Функция read_text

Функция читает файл целиком и возвращает его содержимое в виде одной строки. По умолчанию используется кодировка UTF-8, но при необходимости можно передать другую кодировку, например encoding="cp1251"

````python
def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    '''Считывает текст по указанному пути

    Args:
        path: Путь к файлу в формате строки или Path
        encoding: Тип кодировки файла (пример: encoding="cp1251"), по умолчанию utf-8

    Returns:
        Прочитанный файл в виде строки
    '''
    p = Path(path)
    return p.read_text(encoding=encoding)
````

Если файл не найден, возникает FileNotFoundError. При несовпадении кодировки возникает UnicodeDecodeError.

2. Функция write_csv

Функция записывает строки в CSV-файл. Перед записью проверяется, что все строки имеют одинаковую длину. Если длины отличаются, вызывается ValueError.

````python
def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    '''Записывает частоты слов в csv файл
    Args:
        rows: Список строк которые нужно внести в файл
        path: Путь к файлу записи
        header: Заголовок файла

    Returns:
        None

    Raises:
        ValueError: Строки разной длины
    '''
    p = Path(path)
    rows = list(rows)
    if rows:
        length = len(rows[0])
        for row in rows:
            if len(row) != length:
                raise ValueError("Строки разной длинны")
            if header is not None:
                if len(header) != length:
                    raise ValueError("Строки разной длинны")

    ensure_parent_dir(path)

    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=',')
        if header is not None:
            w.writerow(header)
        for r in rows:
            w.writerow(r)
````

Если передан параметр header, он записывается первой строкой файла.

3. Функция ensure_parent_dir

Функция проверяет наличие родительской папки и создает ее вместе со всеми отсутствующими вложенными папками

````python
def ensure_parent_dir(path):
    """Создаёт папку для файла, если её ещё нет."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
````

<img width="214" height="81" alt="Снимок экрана — 2026-10-18 в 18 00 03" src="https://github.com/user-attachments/assets/b8b8b597-7135-4336-8427-096712e2111b" />


Рис. 1. Результат записи данных в CSV-файл.

Задание B — скрипт статистики src/lab04/text_report.py

Скрипт читает текстовые файлы, использует функции normalize, tokenize, count_freq и top_n из лабораторной работы №3, а затем сохраняет частоты слов в CSV-файлы.

Исходный код src/lab04/text_report.py

````python

import argparse
from pathlib import Path

from src.lab04.io_txt_csv import read_text, write_csv
from src.lib.text import normalize, tokenize, top_n, count_freq

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "lab04"

DEFAULT_INPUT = DATA_DIR / 'input.txt'
DEFAULT_REPORT = DATA_DIR / 'report.csv'
DEFAULT_PER_FILE = DATA_DIR / 'report_per_file.csv'
DEFAULT_TOTAL = DATA_DIR / 'report_total.csv'

parser = argparse.ArgumentParser(description='Считает частоты слов в текстовых файлах и сохраняет отчёты в CSV.')
parser.add_argument("--in", nargs = "+", dest = "input_files", help = "Входные текстовые файлы (один или несколько)" \
"Если не указан, берётся data/lab04/input.txt")
parser.add_argument("--out", nargs = "+", dest = "output_files", help = "Файл для отчёта в режиме одного файла "
         "Если не указан, пишется в data/lab04/report.csv "
         "При нескольких входных файлах игнорируется (см. --per-file и --total)"
)
parser.add_argument(
    '--encoding', default='utf-8',
    help='Кодировка входных файлов (по умолчанию: %(default)s) '
)
parser.add_argument(
    '--per-file', default=str(DEFAULT_PER_FILE),
    help='CSV с частотами по каждому файлу отдельно (по умолчанию: %(default)s) '
)
parser.add_argument(
    '--total', default=str(DEFAULT_TOTAL),
    help='CSV с суммарными частотами по всем файлам (по умолчанию: %(default)s) '
)

args = parser.parse_args()


if args.input_files is None:
    text = read_text(str(DEFAULT_INPUT), encoding=args.encoding)
    tokens = tokenize(normalize(text))
    words_cnt = count_freq(tokens)

    path = str(DEFAULT_REPORT) if args.output_files is None else args.output_files[0]
    write_csv(top_n(words_cnt, len(words_cnt)), path, header=("word", "count"))

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(words_cnt)}")
    print("Топ-5:")
    for word, count in top_n(words_cnt, 5):
        print(f"{word}: {count}")
else:
    # region Для много файлов
    per_file = []  # Здесь лежат данные в формате [file_path, word, count]
    all_cnt = {}   # А тут лежит словарь где указаны частоты всех слов

    for file_path in sorted(args.input_files):  # Идем по файлам в алфавитном порядке
        text = read_text(file_path, encoding=args.encoding)
        normal_text = normalize(text)
        tokens = tokenize(normal_text)
        words_cnt = count_freq(tokens)
        top_all_words = top_n(words_cnt, len(words_cnt))

        for word, count in top_all_words:
            per_file.append([file_path, word, count])

        for word, count in words_cnt.items():
            all_cnt[word] = all_cnt.get(word, 0) + count
    # endregion

    # region Итоговая запись
    s_cnt = top_n(all_cnt, len(all_cnt))  # Это чтобы отсортировать словарь
    write_csv(per_file, args.per_file, header=('file', 'word', 'count'))
    write_csv(list(s_cnt), args.total, header=('word', 'count'))

    total_words = sum(all_cnt.values())
    unique_words = len(s_cnt)

    print(f'Всего слов: {total_words} \n \nУникальных слов: {unique_words}')

    top5 = s_cnt[:5]
    if top5:
        max_len = max(max([len(word[0]) for word in top5]), len('слово'))
    else:
        max_len = len('слово')

    head = f'{"слово":<{max_len}} | частота'

    print(head)
    print('-' * len(head))
    for top in top5:
        print(f'{top[0]:<{max_len}} | {top[1]}')
    print('...')
````

Скрипт поддерживает следующие параметры:

--in — один или несколько входных файлов. Если параметр не указан, используется data/lab04/input.txt;

--out — путь к отчету для режима одного файла;

--encoding — кодировка входных файлов, по умолчанию utf-8;

--per-file — путь к отчету по отдельным файлам в режиме нескольких файлов;

--total — путь к сводному отчету в режиме нескольких файлов.


Пример запуска для одного файла:

python3.12 -m src.lab04.text_report

В этом режиме читается data/lab04/input.txt, а результат записывается в data/lab04/report.csv.

<img width="324" height="134" alt="Снимок экрана — 2026-10-18 в 18 16 33" src="https://github.com/user-attachments/assets/4cef4803-a62d-40f8-abfe-21efcebee703" />

Рис. 2. Результат запуска скрипта для одного входного файла.

Пример запуска для нескольких файлов

python3.12 -m src.lab04.text_report --in data/lab04/a.txt data/lab04/b.txt

В этом режиме отдельно создаются report_per_file.csv и report_total.csv. В консоли выводятся общее количество слов, число уникальных слов и пять самых частотных слов. Для пустого набора слов скрипт также выполняется без ошибки.

<img width="329" height="164" alt="Снимок экрана — 2026-10-17 в 17 04 29" src="https://github.com/user-attachments/assets/d3e91354-56c2-45a1-ad7c-0f95d743bf7e" />

Рис. 3. Результат запуска скрипта для нескольких входных файлов.

Отчет по каждому файлу

````
file,word,count
data/lab04/a.txt,мир,1
data/lab04/a.txt,привет,1
data/lab04/b.txt,привет,2
````

<img width="266" height="113" alt="Снимок экрана — 2026-10-18 в 18 24 22" src="https://github.com/user-attachments/assets/eacd922c-a9f3-4904-b290-3f170befb323" />


Рис. 4. Содержимое отчета report_per_file.csv.

Сводный отчет


<img width="244" height="88" alt="Снимок экрана — 2026-10-18 в 18 26 14" src="https://github.com/user-attachments/assets/4dd6c2cf-dc5b-40db-8b56-3993d6b4e947" />

Рис. 5. Содержимое сводного отчета report_total.csv.





