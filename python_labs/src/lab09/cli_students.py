
"""ЛР9: консольная утилита для работы с хранилищем студентов.
 
Тонкий слой над group.py: разобрать аргументы → вызвать функцию → напечатать.
Логики работы с данными здесь нет.
 
Запуск (из корня репозитория):
    python -m src.lab09.cli_students list --sort gpa
    python -m src.lab09.cli_students add --fio "Иванов Иван" --birthdate 2007-10-10 --group БИВТ-26-6-1 --gpa 4.3
 
Коды возврата:
    0 — всё хорошо;
    1 — ошибка в данных или запись не найдена;
    2 — неправильный вызов (ставит argparse или cmd_update).
"""


import argparse
import sys

from src.lab08.models import format_student
from src.lab09 import group

DEFAULT_DB = "data/lab09/students.csv"


def cmd_add(args):
    """Подкоманда add: добавить студента.

    Собирает запись из опций --fio, --birthdate, --group, --gpa и передаёт
    её в ``group.add_student``. Печатает добавленную запись.

    Args:
        args: результат разбора аргументов (``argparse.Namespace``).

    Returns:
        0 — студент добавлен. Ошибки (неверные данные, дубликат) не ловит,
        их обрабатывает ``main``.
    """
    student = {"fio": args.fio, "birthdate": args.birthdate,
               "group": args.group, "gpa": args.gpa}
    group.add_student(args.db, student)
    print(f"Добавлен: {format_student(student)}")
    return 0


def cmd_list(args):
    """Подкоманда list: вывести всех студентов.

    Печатает по одной записи на строку через ``format_student``.
    С опцией --sort fio|gpa список сортируется.

    Args:
        args: результат разбора аргументов (``argparse.Namespace``).

    Returns:
        0 — всегда; пустая база — тоже нормальный ответ.
    """
    students = group.list_students(args.db, sort_by=args.sort)
    if not students:
        print("(список пуст)")
    for s in students:
        print(format_student(s))
    return 0


def cmd_find(args):
    """Подкоманда find: найти студентов по подстроке в ФИО (--q).

    Поиск без учёта регистра. Печатает найденных по одному на строку.

    Args:
        args: результат разбора аргументов (``argparse.Namespace``).

    Returns:
        0 — всегда; «никого не нашли» — это ответ, а не ошибка.
    """
    found = group.find_students(args.db, args.q)
    if not found:
        print(f"Никого не найдено по запросу {args.q!r}")
    for s in found:
        print(format_student(s))
    return 0


def cmd_remove(args):
    """Подкоманда remove: удалить всех студентов с таким ФИО (--fio).

    Печатает, сколько записей удалено.

    Args:
        args: результат разбора аргументов (``argparse.Namespace``).

    Returns:
        0 — всегда; удалено ноль — тоже нормальный ответ.
    """
    n = group.remove_student(args.db, args.fio)
    print(f"Удалено записей: {n}")
    return 0


def cmd_update(args):
    """Подкоманда update: изменить поля первого студента с таким ФИО.

    В ``group.update_student`` передаются только те поля из
    --birthdate, --group, --gpa, которые пользователь указал.

    Args:
        args: результат разбора аргументов (``argparse.Namespace``).

    Returns:
        0 — запись обновлена;
        1 — студент не найден;
        2 — не указано ни одного поля для изменения.
    """
    fields = {k: getattr(args, k) for k in ("birthdate", "group", "gpa")
              if getattr(args, k) is not None}
    if not fields:
        print("Ошибка: укажите хотя бы одно поле: --gpa, --group или --birthdate",
              file=sys.stderr)
        return 2
    if group.update_student(args.db, args.fio, **fields):
        print(f"Обновлён: {args.fio}")
        return 0
    print(f"Студент {args.fio!r} не найден", file=sys.stderr)
    return 1


def cmd_stats(args):
    """Подкоманда stats (★): вывести статистику по студентам.

    Печатает количество студентов, минимальный, максимальный и средний
    GPA, число студентов в каждой группе и топ-5 по GPA.

    Args:
        args: результат разбора аргументов (``argparse.Namespace``).

    Returns:
        0 — всегда; для пустой базы печатается только количество.
    """
    st = group.stats(args.db)
    print(f"Всего студентов: {st['count']}")
    if st["count"]:
        print(f"GPA: min {st['min_gpa']:.2f}, max {st['max_gpa']:.2f}, "
              f"средний {st['avg_gpa']:.2f}")
        print("По группам:")
        for g, n in st["groups"].items():
            print(f"  {g}: {n}")
        print("Топ-5:")
        for i, s in enumerate(st["top_5_students"], start=1):
            print(f"  {i}. {s['fio']} — {s['gpa']:.2f}")
    return 0


def build_parser():
    """Создать парсер аргументов с подкомандами.

    Подкоманды: add, list, find, remove, update, stats. Общая опция --db
    (путь к хранилищу, по умолчанию ``DEFAULT_DB``) подключена к каждой
    подкоманде через родительский парсер. Каждой подкоманде через
    ``set_defaults(func=...)`` назначен свой обработчик ``cmd_...``.

    Returns:
        Готовый ``argparse.ArgumentParser``.
    """
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", default=DEFAULT_DB,
                        help=f"путь к CSV-хранилищу (по умолчанию {DEFAULT_DB})")

    parser = argparse.ArgumentParser(prog="cli_students", description="CRUD над students.csv")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", parents=[common], help="добавить студента")
    p.add_argument("--fio", required=True)
    p.add_argument("--birthdate", required=True, help="ГГГГ-ММ-ДД")
    p.add_argument("--group", required=True)
    p.add_argument("--gpa", required=True, type=float)
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", parents=[common], help="показать всех")
    p.add_argument("--sort", choices=["fio", "gpa"])
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("find", parents=[common], help="поиск по подстроке в ФИО")
    p.add_argument("--q", required=True)
    p.set_defaults(func=cmd_find)

    p = sub.add_parser("remove", parents=[common], help="удалить по ФИО")
    p.add_argument("--fio", required=True)
    p.set_defaults(func=cmd_remove)

    p = sub.add_parser("update", parents=[common], help="изменить поля записи")
    p.add_argument("--fio", required=True)
    p.add_argument("--gpa", type=float)
    p.add_argument("--group")
    p.add_argument("--birthdate")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("stats", parents=[common], help="статистика по группе (★)")
    p.set_defaults(func=cmd_stats)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, KeyError) as e:
        msg = e.args[0] if e.args else e
        print(f"Ошибка: {msg}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())