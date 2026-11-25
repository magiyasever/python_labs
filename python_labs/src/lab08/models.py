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


def make_student(fio: str, birthdate: str | None = None, group: str | None = None,
                 gpa: int | float | None = None) -> dict:
    """Создать запись студента: проверить через validate_student и собрать словарь.

    Можно вызвать двумя способами:
        make_student("Иванов Иван", "2007-05-14", "БИВТ-26-6-1", 4)
        make_student("Иванов Иван, 2007-05-14, БИВТ-26-6-1, 4")   # одной строкой

    Args:
        fio: ФИО — или вся запись строкой 'ФИО, ГГГГ-ММ-ДД, группа, gpa',
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
    if birthdate is None and group is None and gpa is None and type(fio) is str:
        # вся запись пришла одной строкой: проверить, затем разложить по полям
        validate_student(fio)
        fio, birthdate, group, gpa = [p.strip() for p in fio.split(",")]
    else:
        validate_student({"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa})
    return {"fio": fio.strip(), "birthdate": birthdate,
            "group": group.strip(), "gpa": float(gpa)}


def student_age(rec: dict, today: date | None = None) -> int:
    """Посчитать полных лет студента на дату today.

    Если день рождения в году today ещё не наступил, год не засчитывается.

    Args:
        rec: запись Student.
        today: дата, на которую считать возраст; по умолчанию — сегодня.

    Returns:
        Число полных лет.
    """
    b = date.fromisoformat(rec["birthdate"])
    if today is None:
        today = date.today()
    age = today.year - b.year
    if (today.month, today.day) < (b.month, b.day):
        age -= 1
    return age


def student_to_dict(rec: dict) -> dict:
    """Вернуть проверенную копию записи для сериализации в JSON.

    Args:
        rec: запись Student.

    Returns:
        Новый словарь с теми же ключами и значениями.

    Raises:
        ValueError: если запись не проходит validate_student.
    """
    validate_student(rec)
    return {
        "fio": rec["fio"],
        "birthdate": rec["birthdate"],
        "group": rec["group"],
        "gpa": rec["gpa"],
    }


def student_from_dict(d: dict) -> dict:
    """Превратить словарь из JSON в проверенную запись Student.

    Берутся ровно ключи STUDENT_FIELDS (лишние отбрасываются),
    gpa приводится к float, все поля проверяются.

    Args:
        d: словарь, прочитанный из JSON.

    Returns:
        Новая запись Student.

    Raises:
        ValueError: если d не словарь, не хватает ключа или значение неверно.
    """
    if type(d) is not dict:
        raise ValueError(f"запись: ожидался словарь, получено {d!r}")
    for key in STUDENT_FIELDS:
        if key not in d:
            raise ValueError(f"нет ключа {key!r}")
    return make_student(d["fio"], d["birthdate"], d["group"], d["gpa"])


def format_student(rec: dict) -> str:
    """Оформить запись в одну строку.

    Args:
        rec: запись Student.

    Returns:
        Строка вида 'Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30'.
    """
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


def update_student(rec: dict, **fields) -> dict:
    """Вернуть новую запись с изменёнными полями; исходная rec не меняется.

    Args:
        rec: исходная запись Student.
        **fields: новые значения полей, например gpa=4.8.

    Returns:
        Новая проверенная запись Student.

    Raises:
        KeyError: если в fields есть поле не из STUDENT_FIELDS.
        ValueError: если новое значение не проходит проверку.
    """
    for key in fields:
        if key not in STUDENT_FIELDS:
            raise KeyError(f"неизвестное поле: {key!r}")
    new = dict(rec)
    new.update(fields)
    validate_student(new)
    return make_student(**new)
