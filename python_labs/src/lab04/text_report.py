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
         
    print(f"Всего слов: {len(tokens)}\n")
    print(f"Уникальных слов: {len(words_cnt)}\n")
    for word, count in top_n(words_cnt, 5):
        print(f"{word}:{count}")
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


