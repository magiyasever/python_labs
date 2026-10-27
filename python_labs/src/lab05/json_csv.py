import csv
import json
import sys
from pathlib import Path

from src.lib.often_func import ensure_parent_dir


def json_to_csv(json_path: str, csv_path: str, delimiter: str = ",") -> None:
    """Конвертирует JSON-файл (список словарей) в CSV-файл.

    Колонки CSV собираются из ключей ВСЕХ записей, в порядке появления.
    Если у записи нет какого-то ключа, ячейка остаётся пустой.

    Args:
        json_path: Путь к JSON-файлу, из которого читаем.
        csv_path: Путь к CSV-файлу, куда пишем.
        delimiter: Разделитель CSV (для русского Excel передайте ";").

    Raises:
        FileNotFoundError: JSON-файл не найден.
        ValueError: Файл не .json; битый JSON (с указанием строки);
            JSON не является непустым списком; элемент списка не словарь;
            в записи есть вложенный список или словарь (CSV плоский).
    """
    jp = Path(json_path)
    cp = Path(csv_path)

    if not jp.is_file():
        raise FileNotFoundError(f"JSON файл не найден: {jp}")
    if jp.suffix.lower() != ".json":
        raise ValueError(f"Указанный файл не формата JSON: {jp}")

    with jp.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Битый JSON: {e.msg} (строка {e.lineno}, столбец {e.colno})") from e
    if not isinstance(data, list) or not data:
        raise ValueError("JSON должен быть непустым списком записей")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы списка JSON должны быть словарями")

    fieldnames = {}
    for number, item in enumerate(data, start=1):
        for key, value in item.items():
            if isinstance(value, (list, dict)):
                raise ValueError(
                    f"Запись №{number}, поле «{key}»: вложенные списки и "
                    f"словари нельзя записать в плоский CSV"
                )
            fieldnames[key] = None

    ensure_parent_dir(cp)
    with cp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames), delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)


def csv_to_json( csv_path: str, json_path: str, numeric_fields: tuple = (), delimiter: str = ",",) -> None:
    """Конвертирует CSV-файл в JSON-файл (список словарей).

    Из CSV всё приходит строками. Колонки из numeric_fields приводятся
    к float один раз, сразу после чтения; остальные остаются строками.

    Args:
        csv_path: Путь к CSV-файлу, из которого читаем.
        json_path: Путь к JSON-файлу, куда пишем.
        numeric_fields: Названия колонок, которые нужно сделать числами.
        delimiter: Разделитель CSV (для русского Excel передайте ";").

    Raises:
        FileNotFoundError: CSV-файл не найден.
        ValueError: Файл не .csv; файл пустой; нет строк с данными;
            в CSV нет колонки из numeric_fields; значение в такой колонке
            не число (ошибка данных, с номером записи).
    """
    cp = Path(csv_path)
    jp = Path(json_path)

    if not cp.is_file():
        raise FileNotFoundError(f"CSV файл не найден: {cp}")
    if cp.suffix.lower() != ".csv":
        raise ValueError(f"Указанный файл не формата CSV: {cp}")

    with cp.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        if reader.fieldnames is None:
            raise ValueError("Файл CSV пустой")
        fieldnames = reader.fieldnames
        data = list(reader) 

    if not data:
        raise ValueError("Файл CSV не содержит данных")

    missing = [name for name in numeric_fields if name not in fieldnames]
    if missing:
        raise ValueError(f"В CSV нет колонок: {', '.join(missing)}")

    for number, row in enumerate(data, start=1):
        for name in numeric_fields:
            try:
                row[name] = float(row[name])
            except (TypeError, ValueError) as e:
                raise ValueError(
                    f"Запись №{number}, колонка «{name}»: "
                    f"не число ({row[name]!r})"
                ) from e

    ensure_parent_dir(jp)
    with jp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    """Точка входа: ошибки превращаем в сообщение в stderr и код выхода 1."""
    try:
        csv_to_json(
    "data/samples/cities.csv",
    "data/out/a.json",
)
    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
