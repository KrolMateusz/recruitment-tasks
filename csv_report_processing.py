import pycountry
import csv
import sys
import pathlib
import datetime


def check_if_file_exists(filename):
    """Exits program if file does not exist.

    :param str filename: name of file
    """
    try:
        pathlib.Path(filename).resolve(strict=True)
    except FileNotFoundError:
        sys.exit(f'File not found: {filename}')


def check_encoding(filename):
    """Recognizes encoding of file, (utf-8 or utf-16).

    :param str filename: name of file
    :return str: encoding type of file
    """
    try:
        with open(filename, encoding='utf-16') as csv_file:
            # if readline does not raise unicode error encoding, then
            # encoding is utf-16
            csv_file.readline()
        return 'utf-16'
    except UnicodeError:
        try:
            with open(filename, encoding='utf-8') as csv_file:
                # if readline does not raise unicode error encoding, then
                # encoding is utf-8
                csv_file.readline()
            return 'utf-8'
        except UnicodeError:
            sys.exit('Wrong encoding type.')


def get_country_code(state_name):
    """Returns code of country based on state or XXX for unknown state.

    :param str state_name: the name of state
    :return str: three letter code country or XXX
    """
    try:
        # if lookup does not raise an error, function returns three letter code
        # of country, else it returns XXX
        return pycountry.subdivisions.lookup(state_name).country.alpha_3
    except LookupError:
        return 'XXX'


def load_data_from_file(filename):
    """Loads and aggregate data from csv file by date and country.

    Data is written in nested dictionary. The key of dictionary is date and
    the value is another dictionary. The key of nested dictionary is code of
    country and the value is list with number of impressions and clicks, e.g.
    {datetime.date(2019, 1, 21): {'GIN': [959, 4], 'AFG': [919, 6]},
    datetime.date(2019, 1, 22): {'GIN': [1251, 12], 'CZE': [139, 1]},
    datetime.date(2019, 1, 23): {'XXX': [777, 2], 'GIN': [593, 2]}}.

    :param str filename: the name of file
    :return dict: dictionary with aggregated data
    """
    encoding_type = check_encoding(filename)
    data = {}
    with open(filename, newline='', encoding=encoding_type) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # if row has more than 4 values, it is omitted and message is
            # written to standard error
            if len(row) != 4:
                sys.stderr.write(f'Row omitted: {len(row)} values instead '
                                 f'of 4 in row: {row}\n')
                continue
            try:
                date, state, impressions, ctr = row
                ctr = float(ctr[:-1])
                if not 0 <= ctr <= 100:
                    sys.stderr.write(f'Row omitted: ctr ({ctr}) is not in '
                                     f'range <0, 100>.')
                country_code = get_country_code(state)
                # date is written in format YYYY/MM/DD
                date = datetime.date(int(date[6:]), int(date[:2]),
                                     int(date[3:5]))
                # inserts date as key and empty dictionary as value, if it was
                # not in dictionary
                data.setdefault(date, {})
                # inserts code of country as key, if it was not in dictionary
                # with [0, 0] as a value
                data[date].setdefault(country_code, [0, 0])
                # adds number of impressions and rounded number of clicks for
                # every code of country
                data[date][country_code][0] += int(impressions)
                data[date][country_code][1] += round(ctr * int(impressions)
                                                     / 100)
            except ValueError as e:
                sys.stderr.write(f'Row omitted, error occurred: {e}\n')
    return data


def write_data_to_file(data, filename):
    """Writes data to csv file with utf-8 encoding.

    :param dict data: dictionary with aggregated data
    :param str filename: name of file to write data
    """
    try:
        # writes a data with utf-8 encoding, and unix line separator
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
    """Writes aggregated data to file given using cli"""
    # if wrong number of arguments is given, program will stop running
    if len(sys.argv) != 3:
        sys.exit(f'To run this program type in command prompt: '
                 f'csv_report_processing.py input_file.csv output_file.csv')
    input_file, output_file = sys.argv[1:]
    check_if_file_exists(input_file)
    data = load_data_from_file(input_file)
    write_data_to_file(data, output_file)


if __name__ == '__main__':
    main()
