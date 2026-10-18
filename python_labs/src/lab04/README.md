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

