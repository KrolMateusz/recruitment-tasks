import pycountry
import csv
import sys
import pathlib


def check_if_file_exists(filename):
    try:
        pathlib.Path(filename).resolve(strict=True)
    except FileNotFoundError as e:
        sys.exit(e)
    else:
        return True


def check_encoding(filename):
    try:
        with open(filename, encoding='utf-8') as csv_file:
            csv_file.readline()
        encoding = 'utf-8'
    except UnicodeError:
        pass
    else:
        try:
            with open(filename, encoding='utf-16') as csv_file:
                csv_file.readline()
            encoding = 'utf-16'
        except UnicodeError:
            pass
        return encoding


def get_country_code(state_name):
    try:
        alpha_3 = pycountry.subdivisions.lookup(state_name).country.alpha_3
        return alpha_3
    except LookupError:
        return 'XXX'


def load_data():
    file = sys.argv[1]
    check_if_file_exists(file)
    encoding_type = check_encoding(file)
    try:
        with open(file, newline='', encoding=encoding_type) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if len(row) != 4:
                    sys.stderr.write(f'{len(row)} values instead of 4 in row: '
                                     f'{row}\n')
                    continue
                date, state_name, impressions, ctr = row
                print(date, state_name, impressions, ctr)
                print(get_country_code(state_name))
    except (FileNotFoundError, UnicodeError) as e:
        sys.stderr.write('Critical error: ' + str(e) + '\n')


def main():
    load_data()


if __name__ == '__main__':
    main()
