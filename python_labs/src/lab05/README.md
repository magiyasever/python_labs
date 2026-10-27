Отчет по лабораторной работе №5 — JSON, CSV и XLSX

Структура лабораторной работы

src/lab05/json_csv.py — преобразование JSON в CSV и CSV в JSON;

src/lab05/csv_xlsx.py — преобразование CSV в XLSX.

Входные примеры находятся в каталоге data/lab05/samples/, а результаты конвертаций — в каталоге data/lab05/out/.

Задание A — JSON ↔ CSV

Модуль json_csv.py содержит две функции.

Функция json_to_csv

````python

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
````
Функция:

проверяет существование входного файла;

проверяет расширение .json;

читает JSON в кодировке UTF-8;

проверяет, что корневой объект является непустым списком словарей;

собирает названия всех ключей в порядке их первого появления;

записывает заголовок и строки в CSV в кодировке UTF-8.

Если в одном из словарей отсутствует ключ, csv.DictWriter записывает в соответствующую ячейку пустое значение.

Пример вызова:

````python
json_to_csv(
    "data/lab05/samples/people.json",
    "data/lab05/out/people_from_json.csv",
)
````
Функция csv_to_json

````python
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

````
Функция:

проверяет существование входного файла;
проверяет расширение .csv;
читает CSV в кодировке UTF-8;
проверяет наличие заголовка и хотя бы одной строки данных;
преобразует каждую строку в словарь;
сохраняет список словарей в JSON с отступом в два пробела.
Пример вызова:

````python
csv_to_json(
    "data/lab05/samples/people.csv",
    "data/lab05/out/people_from_csv.json",
)
````

Запуск модуля JSON ↔ CSV

Из корня репозитория:

python -m src.lab05.json_csv
При таком запуске создаются:

data/lab05/out/people_from_csv.json;
data/lab05/out/people_from_json.csv.
Задание B — CSV → XLSX

Модуль csv_xlsx.py содержит функцию:
````python

def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    '''Конвертирует CSV файл в формат XLSX.

        Args:
            csv_path: Путь к исходному CSV файлу
            xlsx_path: Путь для сохранения XLSX файла

        Returns:
            None

        Raises:
            FileNotFoundError:
                Указанный CSV файл не найден
            ValueError:
                Указанный файл не формата CSV
                Файл CSV пустой
        '''
    cp = Path(csv_path)
    xlp = Path(xlsx_path)

    if not cp.exists():
        raise FileNotFoundError("Указанный CSV файл не найден")

    if cp.suffix.lower() != '.csv':
        raise ValueError("Указанный файл не формата CSV")

    with cp.open('r', newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))

    if not reader:
        raise ValueError("Файл CSV пустой")

    wb = Workbook()
    ws = wb.active
    assert ws is not None
    ws.title = "Sheet1"
    for row in reader:
        ws.append(row)

    for col in ws.columns:
        max_len = 0
        letter = col[0].column_letter

        for cell in col:
            if cell.value and len(str(cell.value)) > max_len:
                max_len = len(str(cell.value))

        ws.column_dimensions[letter].width = max(max_len, 8)

    ensure_parent_dir(xlp)
    wb.save(xlp)
````
Функция:

проверяет существование CSV-файла;
проверяет расширение .csv;
читает строки в кодировке UTF-8;
создаёт книгу Excel с помощью openpyxl;
добавляет строки CSV на лист Sheet1;
рассчитывает ширину столбцов;
сохраняет результат по указанному пути.

Пример вызова:
````python
csv_to_xlsx(
    "data/lab05/samples/people.csv",
    "data/lab05/out/people.xlsx",
)
````
Запуск модуля CSV → XLSX
````
python -m src.lab05.csv_xlsx
````
После запуска создаётся файл data/lab05/out/people.xlsx.

Обработка ошибок

Входные функции явно сообщают об ошибках:

FileNotFoundError — входной файл не найден;
ValueError — расширение файла не соответствует ожидаемому формату;
ValueError — JSON пустой, имеет неподдерживаемую структуру или содержит элементы не-словари;
ValueError — CSV пустой или не содержит строк данных.
Родительский каталог выходного файла создаётся функцией ensure_parent_dir() из src.lib.often_func, поэтому выходные каталоги должны создаваться автоматически.

Примеры данных и результаты

Для демонстрации используются следующие файлы:

data/lab05/samples/people.json — список людей в формате JSON;
data/lab05/samples/people.csv — те же данные в формате CSV;
data/lab05/samples/cities.csv — дополнительный CSV с городами;
data/lab05/out/people_from_json.csv — результат JSON → CSV;
data/lab05/out/people_from_csv.json — результат CSV → JSON;
data/lab05/out/people.xlsx — результат CSV → XLSX.
Проверка результатов

1. JSON → CSV

   
<img width="272" height="166" alt="Снимок экрана — 2026-10-27 в 11 42 36" src="https://github.com/user-attachments/assets/c05d5062-7d7d-4324-900a-0a4eb671dedd" />

Рис. 1. Результат преобразования JSON в CSV

2. CSV → JSON

<img width="258" height="511" alt="Снимок экрана — 2026-10-27 в 11 49 42" src="https://github.com/user-attachments/assets/8598dec6-6612-4575-bb74-411ee72ddac7" />

Рис. 2. Результат преобразования CSV в JSON.

3. CSV → XLSX

<img width="327" height="210" alt="Снимок экрана — 2026-10-27 в 11 52 55" src="https://github.com/user-attachments/assets/11287e2c-3b4c-47c7-8d24-7c64aa224de3" />

Рис. 3. Результат преобразования CSV в XLSX
