import argparse
from pathlib import Path
from src.lib.text import normalize, tokenize, count_freq, top_n

def main():

    '''Выводит статистику по тексту или выводит содержимое файла

    Args:
        cat: Вывод содержимого
            --input: Путь к файлу !обязательно!
            -n: Нумерация строк (по умолчанию False)
        
        stats: Вывод частот слов
            --input: Путь к файлу !обязательно!
            -top: Количество отображаемых элементов в топе 
    
    Returns:
        None: Выводит в консоль
    
    Raises:
        cat:
            FileNotFoundError: Нет файла по указанному пути

        stats:
            ValueError: Топ не может быть отрицательным
            FileNotFoundError: Нет файла по указанному пути

        Все остальные ошибки вызываются и обрабатываются в вызываемых функциях
    '''
    parser = argparse.ArgumentParser(description="CLI‑утилиты лабораторной №6")
    subparsers = parser.add_subparsers(dest="command")

    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True)
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    stats_parser = subparsers.add_parser("stats", help="Частоты слов")
    stats_parser.add_argument("--input", required=True)
    stats_parser.add_argument("--top", type=int, default=5)

    args = parser.parse_args()

    if args.command == "cat":
        path = Path(args.input)
        if not path.exists():
            raise FileNotFoundError(f"Файл {args.input} не найден")
        with open(path, "r", encoding="utf-8", newline="") as f:
            data = f.readlines()
        if args.n:
            for i, line in enumerate(data, start=1):
                print(f"{i}: {line}", end="")
        else:
            print("".join(data), end="")

    elif args.command == "stats":
        path = Path(args.input)
        if not path.exists():
            raise FileNotFoundError(f"Файл {args.input} не найден")
        if args.top <= 0:
            raise ValueError("Параметр --top должен быть положительным числом")
        with open(path, "r", encoding="utf-8", newline="") as f:
            data = f.read()
        normalized_text = normalize(data)
        tokens = tokenize(normalized_text)
        freq_dict = count_freq(tokens)
        top_words = top_n(freq_dict,int(args.top))

        if top_words:
            max_len = max(max([len(word[0]) for word in top_words]), len('слово'))
        else:
            max_len = len('слово')
        head = f'{"слово":<{max_len}} | частота'

        print(head)
        print('-' * len(head))
        for top in top_words:
            print(f'{top[0]:<{max_len}} | {top[1]}')
        print('...')