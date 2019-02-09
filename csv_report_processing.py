import pycountry
import csv
import sys


def lookup(state_name):
    try:
        alpha_3 = pycountry.subdivisions.lookup(state_name).country.alpha_3
        return alpha_3
    except LookupError:
        return 'XXX'


def load_data():
    try:
        with open('input.csv', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for date, state_name, impressions, ctr in csv_reader:
                print(date, state_name, impressions, ctr)
                print(lookup(state_name))
    except (FileNotFoundError, UnicodeError) as e:
        sys.stdout.write('Error: ' + str(e) + '\n')


def main():
    load_data()


if __name__ == '__main__':
    main()
