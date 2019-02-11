import pycountry
import csv
import sys
import pathlib
import datetime


def check_if_file_exists(filename):
    try:
        pathlib.Path(filename).resolve(strict=True)
    except FileNotFoundError:
        sys.exit(f'File not found: {filename}')


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


def load_data_from_file(filename):
    encoding_type = check_encoding(filename)
    try:
        data = {}
        with open(filename, newline='', encoding=encoding_type) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if len(row) != 4:
                    sys.stderr.write(f'Row omitted: {len(row)} values instead '
                                     f'of 4 in row: {row}\n')
                    continue
                date, state, impressions, ctr = row
                state = get_country_code(state)
                date = datetime.date(int(date[6:]), int(date[:2]),
                                     int(date[3:5]))
                data.setdefault(date, {})
                data[date].setdefault(state, [0, 0])
                data[date][state][0] += int(impressions)
                data[date][state][1] += round(float(ctr[:-1])*int(impressions)
                                              / 100)
        return data
    except UnicodeError as e:
        sys.stderr.write(f'Critical error: {e}')


def write_data_to_file(data, filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',',
                                    lineterminator='\n')
            for date in sorted(data.keys()):
                for country_code in sorted(data[date]):
                    csv_writer.writerow((date, country_code,
                                        *data[date][country_code]))
    except KeyError as e:
        sys.stderr.write(e)


def main():
    if len(sys.argv) != 3:
        sys.exit(f'To run this program type: csv_report_processing.py '
                 f'input_file.csv output_file.csv')
    input_file, output_file = sys.argv[1:]
    check_if_file_exists(input_file)
    data = load_data_from_file(input_file)
    write_data_to_file(data, output_file)


if __name__ == '__main__':
    main()
