import argparse
from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx
from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx

def main():

    ''' Конвертирует CLI

    Args:
        json2csv: Переводит JSON в CSV
            --in: Путь к входному JSON !обязательно!
            --out: Путь к выходному CSV !обязательно!

        csv2json: Переводит CSV в JSON
            --in: Путь к входному CSV !обязательно!
            --out: Путь к выходному JSON !обязательно!

        csv2xlsx: Переводит JSON в CSV
            --in: Путь к входному CSV !обязательно!
            --out: Путь к выходному XLSX !обязательно!
    
    Returns: 
        None: Изменяются файлы по указанным путям
    '''
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(dest="cmd")

    p1 = sub.add_parser("json2csv")
    p1.add_argument("--in", dest="input", required=True)
    p1.add_argument("--out", dest="output", required=True)

    p2 = sub.add_parser("csv2json")
    p2.add_argument("--in", dest="input", required=True)
    p2.add_argument("--out", dest="output", required=True)

    p3 = sub.add_parser("csv2xlsx")
    p3.add_argument("--in", dest="input", required=True)
    p3.add_argument("--out", dest="output", required=True)

    args = parser.parse_args()

    if args.cmd == "json2csv":
        json_to_csv(args.input, args.output)
    elif args.cmd == "csv2json":
        csv_to_json(args.input, args.output)
    elif args.cmd == "csv2xlsx":
        csv_to_xlsx(args.input, args.output)

if __name__ == '__main__':
    main()