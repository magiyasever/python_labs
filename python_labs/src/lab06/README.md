# Отчет по лабораторной работе №6

## Задание A — текстовые CLI-утилиты

Модуль `cli_text.py` содержит подкоманды `cat` и `stats`.

### Подкоманда `cat`

Подкоманда выводит содержимое текстового файла построчно.

```bash
python -m src.lab06.cli_text cat --input data/lab04/input.txt
```

Для нумерации строк используется флаг `-n`:

```bash
python -m src.lab06.cli_text cat --input data/lab04/input.txt -n
```

Параметры:

- `--input` — обязательный путь к входному файлу;
- `-n` — необязательный флаг нумерации строк.

<img width="210" height="114" alt="lab06 -n" src="https://github.com/user-attachments/assets/9c352d19-e237-48ce-98c6-f8aa0a9f97b4" />

*Рис. 1. Работа подкоманды `cat` с флагом `-n`.*

### Подкоманда `stats`

Подкоманда подсчитывает частоты слов в текстовом файле. Для обработки используются функции из [src/lib/text.py](src/lib/text.py):

1. `normalize()` — нормализация текста;
2. `tokenize()` — выделение слов;
3. `count_freq()` — подсчёт частот;
4. `top_n()` — сортировка и выбор наиболее частых слов.

Запуск с количеством слов по умолчанию:

```bash
python -m src.lab06.cli_text stats --input data/lab04/input.txt
```

Запуск с собственным размером топа:

```bash
python -m src.lab06.cli_text stats --input data/lab04/input.txt --top 5
```

Параметры:

- `--input` — обязательный путь к текстовому файлу;
- `--top` — необязательное количество слов в топе (по умолчанию 5).


<img width="139" height="103" alt="stats" src="https://github.com/user-attachments/assets/5e9f90e7-20d8-4ca1-b079-d4db3f8e478d" />

*Рис. 2. Работа подкоманды `stats`.*

## Задание B — CLI-конвертеры

Модуль `cli_convert.py` предоставляет три подкоманды. Внутри используются функции из лабораторной работы №5:

- `json_to_csv()` из `src.lab05.json_csv`;
- `csv_to_json()` из `src.lab05.json_csv`;
- `csv_to_xlsx()` из `src.lab05.csv_xlsx`.

Для всех конвертеров обязательны параметры:

- `--in` — путь к входному файлу;
- `--out` — путь к выходному файлу.

### Подкоманда `json2csv`

Преобразует JSON со списком словарей в CSV:

```bash
python -m src.lab06.cli_convert json2csv \
  --in data/samples/people.json \
  --out data/out/people_from_json.csv
```

<img width="436" height="115" alt="Снимок экрана — 2026-11-02 в 19 09 43" src="https://github.com/user-attachments/assets/49b45673-38f8-4d03-8600-7edd477b2b58" />

*Рис. 3. Справка по подкоманде `json2csv`.*


<img width="232" height="146" alt="json2csv" src="https://github.com/user-attachments/assets/34faa684-2734-4062-a43a-12c0541dbb5d" />

*Рис. 4. Результат запуска `json2csv`.*


### Подкоманда `csv2json`

Преобразует CSV с заголовком в JSON-список словарей:

```bash
python -m src.lab06.cli_convert json2csv \
  --in data/samples/people.json \
  --out data/out/people_from_json.csv
```


<img width="302" height="520" alt="csv2json" src="https://github.com/user-attachments/assets/f0662446-e520-466e-933a-834b4312bb87" />

*Рис. 5. Результат запуска `csv2json`.*

### Подкоманда `csv2xlsx`

Преобразует CSV в таблицу XLSX:


```bash
python -m src.lab06.cli_convert csv2xlsx `
  --in data\lab05\samples\people.csv `
  --out data\lab05\out\people.xlsx
```

<img width="291" height="213" alt="csv2xlsx" src="https://github.com/user-attachments/assets/84b433d9-2efc-4a0a-b67a-7e2b78b6a982" />


*Рис. 6. Результат запуска `csv2xlsx`.*


### Справка `--help`

Справка всего CLI:

```bash
python -m src.lab06.cli_text --help
python -m src.lab06.cli_convert --help
```

Справка отдельных подкоманд:

```bash
python -m src.lab06.cli_text cat --help
python -m src.lab06.cli_text stats --help
python -m src.lab06.cli_convert json2csv --help
python -m src.lab06.cli_convert csv2json --help
python -m src.lab06.cli_convert csv2xlsx --help
```

<img width="395" height="165" alt="cli_text py  -h" src="https://github.com/user-attachments/assets/5e719eca-d24f-4d08-8bc6-3977118da55f" />

*Рис. 7. Справка текстовых подкоманд.*

<img width="425" height="126" alt="cli_convert py  -h" src="https://github.com/user-attachments/assets/60e36716-a5ea-463d-bc25-cbec4ed923b5" />


*Рис. 8. Справка конвертеров.*



### Обработка ошибок

При отсутствии входного файла программы вызывают FileNotFoundError с понятным сообщением о пути к файлу.

Ошибки формата входных файлов и пустых файлов обрабатываются функциями из лабораторных работ №4 и №5. Ошибки обязательных аргументов и неизвестных параметров обрабатываются самим argparse, который выводит сообщение об ошибке и справку по использованию команды.


### Проверка работы

Для проверки были выполнены следующие сценарии:

1. `cat --input data/samples/people.csv -n` — вывод файла с номерами строк;
2. `stats --input data/samples/people.txt --top 5` — вывод пяти наиболее частых слов;
3. `json2csv` — конвертация JSON в CSV;
4. `csv2json` — конвертация CSV в JSON;
5. `csv2xlsx` — конвертация CSV в XLSX;
6. `--help` для общего CLI и каждой подкоманды.

Результаты конвертаций сохраняются в `data/out/`, а скриншоты запусков находятся в `images/lab06/`.

## Зависимости

Сам CLI использует стандартный модуль `argparse`, а также `pathlib` и функции из предыдущих лабораторных работ. Для команды `csv2xlsx` транзитивно требуется `openpyxl`, потому что она вызывает реализацию CSV → XLSX из ЛР5.

Установка зависимостей из корня репозитория:

```bash
python -m pip install -r requirements.txt
```




