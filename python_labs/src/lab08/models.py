"""ЛР8. Модель Student: запись-словарь, конструктор, валидация.

Запись Student — словарь ровно с ключами STUDENT_FIELDS:
    fio       — str, непустая строка
    birthdate — str, формат ГГГГ-ММ-ДД, дата существует и не в будущем
    group     — str, непустая строка
    gpa       — float, 0 <= gpa <= 5

Запуск демонстрации из корня репозитория:  python -m src.lab08.models
"""

from datetime import date

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def validate_student(rec: dict | str) -> None:
    """Проверить запись. Все правила проверки живут здесь, в одном месте.

    Принимает запись-словарь или запись одной строкой
    'ФИО, ГГГГ-ММ-ДД, группа, gpa'. Ничего не возвращает:
    если всё хорошо — молча завершается, если нет — бросает ValueError.

    Args:
        rec: словарь с ключами STUDENT_FIELDS или строка из 4 значений через запятую.

    Raises:
        ValueError: если rec не словарь и не строка, у строки не 4 значения
            или gpa в ней не число, ключи словаря не совпадают с STUDENT_FIELDS,
            или какое-либо значение неверно (в сообщении — поле и значение).
    """
    # запись одной строкой: проверяем формат строки, потом поля как у словаря
    if type(rec) is str:
        parts = [p.strip() for p in rec.split(",")]
        if len(parts) != 4:
            raise ValueError(
                f"ожидалось 4 значения через запятую "
                f"(ФИО, дата, группа, gpa), получено {len(parts)}: {rec!r}")
        fio, birthdate, group, gpa_text = parts
        try:
            gpa = float(gpa_text)
        except ValueError:
            raise ValueError(f"gpa: ожидалось число, получено {gpa_text!r}") from None
        validate_student({"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa})
        return

    if type(rec) is not dict:
        raise ValueError(f"rec: ожидался словарь или строка, получено {rec!r}")
    if set(rec) != set(STUDENT_FIELDS):
        raise ValueError(f"rec: ожидались ключи {STUDENT_FIELDS}, получены {tuple(rec)!r}")

    fio, birthdate, group, gpa = rec["fio"], rec["birthdate"], rec["group"], rec["gpa"]

    if type(fio) is not str or not fio.strip():
        raise ValueError(f"fio: ожидалась непустая строка, получено {fio!r}")
    if type(group) is not str or not group.strip():
        raise ValueError(f"group: ожидалась непустая строка, получено {group!r}")

    if (type(birthdate) is not str or len(birthdate) != 10
            or birthdate[4] != "-" or birthdate[7] != "-"):
        raise ValueError(f"birthdate: ожидался формат ГГГГ-ММ-ДД, получено {birthdate!r}")
    try:
        born = date.fromisoformat(birthdate)
    except ValueError:
        raise ValueError(f"birthdate: неверная дата {birthdate!r}") from None
    if born > date.today():
        raise ValueError(f"birthdate: дата в будущем {birthdate!r}")

    if type(gpa) not in (int, float):
        raise ValueError(f"gpa: ожидалось число, получено {gpa!r}")
    if not (0 <= gpa <= 5):
        raise ValueError(f"gpa: ожидалось 0..5, получено {gpa!r}")


def make_student(fio: str | dict, birthdate: str | None = None, group: str | None = None,
                 gpa: int | float | None = None) -> dict:
    """Создать запись студента: проверить через validate_student и собрать словарь.

    Можно вызвать тремя способами:
        make_student("Иванов Иван", "2007-05-14", "БИВТ-26-6-1", 4)
        make_student("Иванов Иван, 2007-05-14, БИВТ-26-6-1, 4")   # одной строкой
        make_student({"fio": ..., "birthdate": ..., "group": ..., "gpa": ...})

    Поэтому make_student — единый вход: остальные функции модели
    прогоняют через неё запись, в каком бы виде она ни пришла.

    Args:
        fio: ФИО — или вся запись (строкой или словарём),
            если остальные аргументы не переданы.
        birthdate: дата рождения строкой ГГГГ-ММ-ДД.
        group: группа.
        gpa: средний балл, int или float.

    Returns:
        Новый словарь с ключами STUDENT_FIELDS; пробелы по краям fio и group
        убраны, gpa приведён к float.

    Raises:
        ValueError: из validate_student, если данные неверны.
    """
    whole = birthdate is None and group is None and gpa is None and type(fio) in (str, dict)
    if whole:
        # вся запись пришла одним аргументом: проверить, затем разложить по полям
        validate_student(fio)
        if type(fio) is str:
            fio, birthdate, group, gpa = [p.strip() for p in fio.split(",")]
        else:
            fio, birthdate, group, gpa = fio["fio"], fio["birthdate"], fio["group"], fio["gpa"]
    else:
        validate_student({"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa})
    return {"fio": fio.strip(), "birthdate": birthdate,
            "group": group.strip(), "gpa": float(gpa)}


def student_age(rec: dict | str, today: date | str | None = None) -> int:
    """Посчитать полных лет студента на дату today.

    Если день рождения в году today ещё не наступил, год не засчитывается.

    Args:
        rec: запись Student — словарь или строка 'ФИО, ГГГГ-ММ-ДД, группа, gpa'.
        today: дата, на которую считать возраст: объект date
            или строка ГГГГ-ММ-ДД; по умолчанию — сегодня.

    Returns:
        Число полных лет.

    Raises:
        TypeError: если today не None, не date и не строка.
        ValueError: если запись неверна, строка today не в формате ГГГГ-ММ-ДД,
            такой даты нет или today раньше даты рождения.
    """
    rec = make_student(rec)   # запись любого вида -> проверенный словарь
    if today is None:
        today = date.today()
    elif type(today) is str:
        if len(today) != 10 or today[4] != "-" or today[7] != "-":
            raise ValueError(f"today: ожидался формат ГГГГ-ММ-ДД, получено {today!r}")
        try:
            today = date.fromisoformat(today)
        except ValueError:
            raise ValueError(f"today: неверная дата {today!r}") from None
    elif not isinstance(today, date):
        raise TypeError(f"today: ожидалась дата или строка ГГГГ-ММ-ДД, получено {today!r}")

    b = date.fromisoformat(rec["birthdate"])
    if (today.year, today.month, today.day) < (b.year, b.month, b.day):
        raise ValueError(f"today: раньше даты рождения {rec['birthdate']!r}")
    age = today.year - b.year
    if (today.month, today.day) < (b.month, b.day):
        age -= 1
    return age


def student_to_dict(rec: dict | str) -> dict:
    """Вернуть проверенную копию записи для сериализации в JSON.

    Args:
        rec: запись Student — словарь или строка 'ФИО, ГГГГ-ММ-ДД, группа, gpa'.

    Returns:
        Новый словарь с ключами STUDENT_FIELDS (не тот же объект, что rec).

    Raises:
        ValueError: если запись неверна.
    """
    return make_student(rec)   # make_student всегда возвращает новый словарь


def student_from_dict(d: dict | str) -> dict:
    """Превратить словарь из JSON в проверенную запись Student.

    Берутся ровно ключи STUDENT_FIELDS (лишние отбрасываются),
    gpa приводится к float, все поля проверяются.
    Строка 'ФИО, ГГГГ-ММ-ДД, группа, gpa' тоже принимается.

    Args:
        d: словарь, прочитанный из JSON, или запись одной строкой.

    Returns:
        Новая запись Student.

    Raises:
        ValueError: если d не словарь и не строка, не хватает ключа
            или значение неверно.
    """
    if type(d) is str:
        return make_student(d)
    if type(d) is not dict:
        raise ValueError(f"запись: ожидался словарь или строка, получено {d!r}")
    for key in STUDENT_FIELDS:
        if key not in d:
            raise ValueError(f"нет ключа {key!r}")
    return make_student(d["fio"], d["birthdate"], d["group"], d["gpa"])


def format_student(rec: dict | str) -> str:
    """Оформить запись в одну строку.

    Args:
        rec: запись Student — словарь или строка 'ФИО, ГГГГ-ММ-ДД, группа, gpa'.

    Returns:
        Строка вида 'Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30'.

    Raises:
        ValueError: если запись неверна.
    """
    rec = make_student(rec)   # запись любого вида -> проверенный словарь
    parts = rec["fio"].split()
    initials = "".join(p[0].upper() + "." for p in parts[1:])
    age = student_age(rec)
    if age % 10 == 1 and age % 100 != 11:
        word = "год"
    elif age % 10 in (2, 3, 4) and age % 100 not in (12, 13, 14):
        word = "года"
    else:
        word = "лет"
    name = f"{parts[0]} {initials}" if initials else parts[0]
    return f"{name} ({rec['group']}), {age} {word}, GPA {rec['gpa']:.2f}"


def update_student(rec: dict | str, **fields) -> dict:
    """Вернуть новую запись с изменёнными полями; исходная rec не меняется.

    Args:
        rec: исходная запись Student — словарь или строка
            'ФИО, ГГГГ-ММ-ДД, группа, gpa'.
        **fields: новые значения полей, например gpa=4.8.

    Returns:
        Новая проверенная запись Student.

    Raises:
        KeyError: если в fields есть поле не из STUDENT_FIELDS.
        ValueError: если исходная запись или новое значение неверны.
    """
    for key in fields:
        if key not in STUDENT_FIELDS:
            raise KeyError(f"неизвестное поле: {key!r}")
    new = make_student(rec)   # проверенная НОВАЯ запись — исходная rec не тронута
    new.update(fields)
    return make_student(new)  # проверить новые значения и привести к единому виду


if __name__ == "__main__":
    s = make_student("Иванов Иван Иванович", "2007-05-14", "БИВТ-26-6-1", 4)
    print(s)
    print(format_student(s))
    print("одной строкой:", make_student("Смирнова Анна, 2008-09-20, БИВТ-26-6-2, 5"))
    print("возраст на 2026-05-13:", student_age(s, date(2026, 5, 13)))

    s2 = update_student(s, gpa=4.8)
    print("s2:", s2["gpa"], "| s не изменилась:", s["gpa"])

    for bad in [("Петров Пётр", "2003-02-30", "БИВТ-26-6-1", 4.0),
                ("Петров Пётр", "2007-05-14", "БИВТ-26-6-1", 7)]:
        try:
            make_student(*bad)
        except ValueError as e:
            print("ValueError:", e)
