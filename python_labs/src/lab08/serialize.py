import csv
import json
from pathlib import Path

from src.lab08.models import (STUDENT_FIELDS, student_to_dict, student_from_dict,
                              format_student)


def students_to_json(students: list[dict], path: str | Path) -> None:
    """Сериализовать список студентов в JSON-файл.

    Каждая запись проверяется и копируется через student_to_dict.
    Файл пишется в utf-8, кириллица как есть, отступ 2.
    Папка для файла создаётся, если её нет.

    Args:
        students: список записей Student.
        path: путь к выходному JSON-файлу (строка или Path).

    Raises:
        ValueError: если какая-либо запись не проходит проверку.
    """
    path = Path(path)
    data = [student_to_dict(student) for student in students]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def students_from_json(path: str | Path, policy: str = "strict") -> list[dict]:
    """Прочитать список студентов из JSON.

    Args:
        path: путь к JSON-файлу.
        policy: "strict" — упасть на первой битой записи,
                "skip" — пропустить битые записи и напечатать отчёт.

    Returns:
        Список проверенных записей Student.

    Raises:
        ValueError: неверная policy, битый JSON, не массив
            или битая запись при policy="strict".
    """
    if policy not in ("strict", "skip"):
        raise ValueError(f"policy: ожидалось 'strict' или 'skip', получено {policy!r}")

    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if type(data) is not list:
        raise ValueError(f"{path.name}: ожидался JSON-массив")

    students = []
    errors = []
    for i, d in enumerate(data, start=1):
        try:
            student = student_from_dict(d)
            students.append(student)
        except ValueError as e:
            if policy == "strict":
                raise ValueError(f"{path.name}: запись {i}: {e}") from None
            errors.append(f"запись {i}: {e}")

    if errors:
        print(f"{path.name}: пропущено записей: {len(errors)}")
        for msg in errors:
            print("  " + msg)

    return students


def students_from_csv(path: str | Path) -> list[dict]:
    """Прочитать список студентов из CSV-файла. Политика — strict.

    Ожидается заголовок fio,birthdate,group,gpa. Из CSV все значения
    приходят строками, поэтому gpa приводится к float здесь, сразу
    после чтения, и только потом запись идёт в student_from_dict.

    Args:
        path: путь к CSV-файлу (строка или Path).

    Returns:
        Список проверенных записей Student.

    Raises:
        FileNotFoundError: если файла нет.
        ValueError: нет нужной колонки, лишние значения в строке,
            gpa не число или запись не проходит проверку
            (в сообщении — номер строки файла).
    """
    path = Path(path)
    students: list[dict] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        # 1. Заголовок: все ли колонки на месте
        header = reader.fieldnames or []
        missing = [name for name in STUDENT_FIELDS if name not in header]
        if missing:
            raise ValueError(f"{path.name}: в заголовке нет колонок {missing}")

        for i, row in enumerate(reader, start=2):   # строка 1 — заголовок
            # 2. Лишние значения в строке (например, 4,5 без кавычек)
            if None in row:
                raise ValueError(
                    f"{path.name}: строка {i}: лишние значения {row[None]!r} "
                    f"(дробь через запятую? пишите 4.5)")

            # 3. gpa из CSV — строка: приводим к float здесь, на границе
            try:
                row["gpa"] = float(row["gpa"])
            except ValueError:
                raise ValueError(
                    f"{path.name}: строка {i}: gpa: ожидалось число, "
                    f"получено {row['gpa']!r}") from None

            # 4. Остальные проверки — как для JSON
            try:
                students.append(student_from_dict(row))
            except ValueError as e:
                raise ValueError(f"{path.name}: строка {i}: {e}") from None
    return students


if __name__ == "__main__":
    DATA = Path("data") / "lab08"

    students = students_from_json(DATA / "students_input.json")
    for s in students:
        print(format_student(s))
    students_to_json(students, DATA / "students_output.json")
    print("записано в", DATA / "students_output.json", ":", len(students))

    print("\nstrict:")
    try:
        students_from_json(DATA / "students_bad.json")
    except ValueError as e:
        print("ValueError:", e)

    print("\nskip:")
    good = students_from_json(DATA / "students_bad.json", policy="skip")
    print("принято:", len(good))

    print("\ncsv:")
    for s in students_from_csv(DATA / "students.csv"):
        print(format_student(s))