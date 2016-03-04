from collections import Counter
from decimal import Decimal
import locale
import csv
import itertools
from matplotlib import pyplot as plt
import numpy

MY_FILE = input('What file should I use?')

def parse(raw_file, delimiter):
    """Parses a raw CSV file to a Json-line object"""

    with open(raw_file, 'r', encoding='latin1') as opened_file:
        csv_data = csv.reader(opened_file, delimiter=delimiter)
        parsed_data = []
        remaining_lines = itertools.islice(csv_data, 7, None)
        fields = next(remaining_lines)
        for row in remaining_lines:
            parsed_data.append(dict(zip(fields, row)))
    return parsed_data

def combine_similar_data(output_data):
    """Search in the column 'Auftraggeber/Empfanger'. If there are more entries
    with the same name sum up the values and remove the second element"""

    copy_list = []
    for dict1, dict2 in itertools.combinations(output_data, 2):
        if (dict1['Auftraggeber/Empfänger'] == dict2['Auftraggeber/Empfänger']
                or
           ('rewe' in dict1['Auftraggeber/Empfänger'].lower()
               and
            'rewe' in dict2['Auftraggeber/Empfänger'].lower())):
            dict1_value = dict1['Betrag']
            dict2_value = dict2['Betrag']
            sum_up = dict1_value + dict2_value
            dict1['Buchung'] = '; '.join((
                dict1['Buchung'],
                dict2['Buchung']))
            dict1['Valuta'] = '; '.join((
                dict1['Valuta'],
                dict2['Valuta']))
            dict1['Buchungstext'] = '; '.join((
                dict1['Buchungstext'],
                dict2['Buchungstext']))
            dict1['Verwendungszweck'] = '; '.join((
                dict1['Verwendungszweck'],
                dict2['Verwendungszweck']))
            dict1['Betrag'] = sum_up
            dict2['Remove'] = 'To be removed'
    for elem in output_data:
        if 'Remove' not in elem:
            copy_list.append(elem)
    return copy_list

def convert_recalled_values(out_entries_data):
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF8')
    for entry in out_entries_data:
        entry['Betrag'] = locale.atof(entry['Betrag'])
    return out_entries_data

def negative_values(file_data):
    out_sums = []
    for entry in file_data:
        if '-' in entry['Betrag']:
            out_sums.append(entry)
    for i in out_sums:
        i['Betrag'] = i['Betrag'].lstrip('-')
    return out_sums

def positive_values(file_data):
    in_sums = []
    for entry in file_data:
        if '-' not in entry['Betrag']:
            in_sums.append(entry)
    return in_sums

def visualise_data(input_data):
    labels = []
    sizes = []
    for entry in input_data:
        labels.append(entry['Auftraggeber/Empfänger'])
        sizes.append(entry['Betrag'])
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()

parsed_file = parse(MY_FILE, ';')
in_values = positive_values(parsed_file)
converted_data = convert_recalled_values(in_values)
final_data = combine_similar_data(converted_data)
visualise_data(final_data)
