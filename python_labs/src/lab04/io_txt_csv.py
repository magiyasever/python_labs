from pathlib import Path
import csv
from typing import Iterable, Sequence

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

def ensure_parent_dir(path):
    """Создаёт папку для файла, если её ещё нет."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


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