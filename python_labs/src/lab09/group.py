"""ЛР9: «база данных» студентов на CSV — функции хранилища и CRUD.

Каждая функция получает путь к CSV-файлу первым аргументом и работает
по схеме «загрузить → изменить → сохранить». Классов нет — только функции.

Формат файла: первая строка — заголовок ``fio,birthdate,group,gpa``,
дальше по одной записи на строку.
"""


import csv
import os
from pathlib import Path

from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student

HEADER = list(STUDENT_FIELDS)
SORT_KEYS = (None, "fio", "gpa")      

def ensure_storage(path: str | Path) -> None:
    """Создать файл-хранилище, если его ещё нет.

    Создаёт недостающие папки и файл с одной строкой-заголовком
    ``fio,birthdate,group,gpa``. Если файл уже существует, ничего не делает.

    Args:
        path: путь к CSV-файлу.
    """
    path = Path(path)
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(",".join(HEADER) + "\n", encoding="utf-8")

def load_students(path: str | Path) -> list[dict]:
    """Прочитать все записи студентов из CSV.

    Если файла нет, он создаётся пустым (с заголовком). Каждая строка
    проверяется и приводится к типам через ``student_from_dict``
    (``gpa`` становится ``float``).

    Args:
        path: путь к CSV-файлу.

    Returns:
        Список записей-словарей в порядке файла.

    Raises:
        ValueError: неверный заголовок; в строке лишние или недостающие
            значения; запись не прошла проверку. В сообщении указан номер строки.
    """
    rows = []
    ensure_storage(path)                       # нет файла → создастся пустой с заголовком
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != HEADER:        # заголовок проверяем ДО чтения строк
            raise ValueError(f"{path}: неверный заголовок, ожидалось {HEADER}, "
                             f"получено {reader.fieldnames!r}")
        for line, row in enumerate(reader, start=2):
            try:
                if None in row:                # значений больше, чем колонок
                    raise ValueError(f"лишние значения: {row[None]!r}")
                if None in row.values():       # значений меньше, чем колонок
                    raise ValueError("не хватает значений")
                row = dict(row)
                try:
                    row["gpa"] = float(row["gpa"])     # из CSV gpa приходит строкой
                except ValueError:
                    raise ValueError(f"gpa: не число: {row['gpa']!r}")
                rows.append(student_from_dict(row))
            except ValueError as e:
                raise ValueError(f"{path}, строка {line}: {e}")
    return rows


def save_students(path: str | Path, students: list[dict]) -> None:
    """Перезаписать файл целиком: заголовок и все записи.

    Сначала проверяет каждую запись, потом пишет во временный файл и
    подменяет им старый (``os.replace``), чтобы ошибка посреди записи
    не испортила базу.

    Args:
        path: путь к CSV-файлу.
        students: список записей-словарей для сохранения.

    Raises:
        ValueError: хотя бы одна запись не прошла ``validate_student``.
    """
    path = Path(path)
    for s in students:
        validate_student(s)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with open(temp, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(students)
    os.replace(temp, path)

def list_students(path: str | Path, sort_by: str | None = None) -> list[dict]:
    """Получить всех студентов (Read), при желании отсортированных.

    Args:
        path: путь к CSV-файлу.
        sort_by: ``None`` — порядок файла; ``"fio"`` — по алфавиту
            (без учёта регистра, ё = е); ``"gpa"`` — по возрастанию балла.

    Returns:
        Новый список записей. Файл не меняется.

    Raises:
        ValueError: неизвестное значение ``sort_by``.
    """
    if sort_by not in SORT_KEYS:
        raise ValueError(f"sort_by: ожидалось одно из {SORT_KEYS}, получено {sort_by!r}")
    students = load_students(path)
    if sort_by is None:
        return students
    if sort_by == "fio":
        return sorted(students, key=lambda s: s["fio"].casefold().replace("ё", "е"))
    return sorted(students, key=lambda s: s["gpa"])


def add_student(path: str | Path, student: dict) -> None:
    """Добавить студента в конец хранилища (Create).

    Args:
        path: путь к CSV-файлу.
        student: запись-словарь с ключами ``fio, birthdate, group, gpa``.

    Raises:
        ValueError: запись не прошла проверку или студент с таким ``fio``
            уже есть. В обоих случаях файл не меняется.
    """
    validate_student(student)
    students = load_students(path)
    if any(s["fio"] == student["fio"] for s in students):
        raise ValueError(f"fio: студент {student['fio']!r} уже есть")
    students.append(dict(student))
    save_students(path, students)


def find_students(path: str | Path, substr: str) -> list[dict]:
    """Найти студентов по подстроке в ФИО (Read).

    Поиск без учёта регистра, буквы ё и е считаются одинаковыми.

    Args:
        path: путь к CSV-файлу.
        substr: подстрока, которую ищем в ``fio``.

    Returns:
        Все подходящие записи; ``[]``, если никого не нашли. Файл не меняется.
    """
    q = substr.casefold().replace("ё", "е")
    return [s for s in load_students(path) if q in s["fio"].casefold().replace("ё", "е")]


def remove_student(path: str | Path, fio: str) -> int:
    """Удалить студентов с таким ФИО (Delete).

    Удаляются ВСЕ записи, у которых ``fio`` точно совпадает с заданным
    (ФИО не уникально). Если никого не нашли, файл не трогается.

    Args:
        path: путь к CSV-файлу.
        fio: ФИО целиком, сравнение точное.

    Returns:
        Количество удалённых записей; ``0``, если никого не нашли.
    """
    students = load_students(path)
    kept = [s for s in students if s["fio"] != fio]
    removed = len(students) - len(kept)
    if removed:
        save_students(path, kept)
    return removed

def update_student(path: str | Path, fio: str, **fields) -> bool:
    """Обновить поля первой записи с таким ФИО (Update).

    Ключи проверяются до работы с файлом. Новая запись проверяется
    через ``student_from_dict``; если проверка не прошла, файл не меняется.

    Args:
        path: путь к CSV-файлу.
        fio: ФИО целиком, сравнение точное. Меняется только первая
            подходящая запись.
        **fields: новые значения полей, например ``gpa=4.9, group="БИВТ-26-6-2"``.

    Returns:
        ``True``, если запись найдена и обновлена, иначе ``False``.

    Raises:
        KeyError: среди ``fields`` есть неизвестное поле.
        ValueError: новая запись не прошла проверку.
    """
    unknown = sorted(set(fields) - set(HEADER))
    if unknown:
        raise KeyError(f"неизвестные поля {unknown}, допустимые: {HEADER}")

    students = load_students(path)
    for i, s in enumerate(students):
        if s["fio"] == fio:
            new = {**s, **fields}
            students[i] = student_from_dict(new)
            save_students(path, students)
            return True
    return False

def stats(path: str | Path) -> dict:
    """Собрать статистику по студентам.

    Args:
        path: путь к CSV-файлу.

    Returns:
        Словарь с ключами:
        ``count`` — число студентов;
        ``min_gpa``, ``max_gpa``, ``avg_gpa`` — минимальный, максимальный
        и средний балл (``None`` для пустой базы);
        ``groups`` — ``{группа: число студентов}``;
        ``top_5_students`` — до пяти записей ``{"fio", "gpa"}`` по убыванию балла.
    """
    students = load_students(path)
    if not students:
        return {"count": 0, "min_gpa": None, "max_gpa": None, "avg_gpa": None,
                "groups": {}, "top_5_students": []}

    gpas = [s["gpa"] for s in students]
    groups = {}
    for s in students:
        groups[s["group"]] = groups.get(s["group"], 0) + 1

    top = sorted(students, key=lambda s: s["gpa"], reverse=True)[:5]
    return {
        "count": len(students),
        "min_gpa": min(gpas),
        "max_gpa": max(gpas),
        "avg_gpa": round(sum(gpas) / len(gpas), 2),
        "groups": groups,
        "top_5_students": [{"fio": s["fio"], "gpa": s["gpa"]} for s in top],
    }