def format_record(rec: tuple[str, str, float]) -> str:

    '''Функция форматирует запись, приводя ее в вид
       "Петров П., гр. IKBO-12, GPA 5.00"

    Args:
        rec: Кортеж в котором содержится ФИО, группа, оценка

    Returns:
        Строку, где указано имя, инициалы, группа, оценка

    Raises:
        TypeError:
            'Запись должна быть кортежем'
            'ФИО и группа должны быть строками'
            'Средний балл должен быть числом'
        ValueError:
            'В кортеже должно быть 3 элемента'
            'ФИО и группа не могут быть пустыми'
            'ФИО должно содержать как минимум имя и фамилию'
            'Средний балл должен быть в диапазоне от 0 до 5'

    '''
    if not isinstance(rec, tuple):
        raise TypeError('Запись должна быть кортежем')
    if len(rec) != 3:
        raise ValueError('В кортеже должно быть 3 элемента')
    fio, group, gpa = rec
    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError("ФИО и группа должны быть строками")
    if not isinstance(gpa, (int, float)) or isinstance(gpa, bool):
        raise TypeError("Средний балл должен быть числом")
    fio = ' '.join(fio.split())
    group = group.strip()
    if fio == "" or group == "":
        raise ValueError("ФИО и группа не могут быть пустыми")
    parts = fio.split()
    if len(parts) < 2 or len(parts) > 3:
        raise ValueError("ФИО должно содержать как минимум имя и фамилию")
    gpa = float(gpa)
    if gpa < 0 or gpa > 5:
        raise ValueError("Средний балл должен быть в диапазоне от 0 до 5")
    surname = parts[0]
    firts_name = parts[1:3]
    surname = surname.capitalize()
    initials = ''
    for name in firts_name:
        initials += name[0].upper() + '.'
    return f"{surname} {initials}, гр. {group}, GPA {gpa:.2f}"

print(f'''
("Иванов Иван Иванович", "BIVT-25", 4.6) -> {format_record(("Иванов Иван Иванович", "BIVT-25", 4.6))}
("Петров Пётр", "IKBO-12", 5.0) -> {format_record(("Петров Пётр", "IKBO-12", 5.0))}
("Петров Пётр Петрович", "IKBO-12", 5.0) -> {format_record(("Петров Пётр Петрович", "IKBO-12", 5.0))}
("  сидорова  анна   сергеевна ", "ABB-01", 3.999) -> {format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999))}
''')

# Вызывает ошибку ValueError
# print(f'("Иванов Иван Иванович", "     ", 4.6) -> {format_record(("Иванов Иван Иванович", "    ", 4.1))}')