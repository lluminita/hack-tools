import locale
import csv
import itertools
from matplotlib import pyplot as plt
import numpy as np

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


def sumup_and_join_values(dict1, dict2):
    sum_up = dict1['Betrag'] + dict2['Betrag']
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
    return dict1, dict2


def sumup_rewe_spendings(data):
    for dict1, dict2 in itertools.combinations(data, 2):
        if ('rewe' in dict1['Auftraggeber/Empfänger'].lower() and
                'rewe' in dict2['Auftraggeber/Empfänger'].lower()):
            sumup_and_join_values(dict1, dict2)
    return data


def sumup_similar_spendings(data):
    """Search in the column 'Auftraggeber/Empfanger'.
    If there are more entries with the same name
    sum up the values and remove the second element"""
    for dict1, dict2 in itertools.combinations(data, 2):
        if (dict1['Auftraggeber/Empfänger'] == dict2['Auftraggeber/Empfänger']):
            sumup_and_join_values(dict1, dict2)
    return data


def remove_old_values(data):
    for elem in data:
        if 'Remove' in elem:
            data.remove(elem)
    return data


def convert_decimal_values(data):
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF8')
    for value in data:
        value['Betrag'] = locale.atof(value['Betrag'])
    return data


def get_expenses(file_data):
    expenses = []
    for expense in file_data:
        if '-' in expense['Betrag']:
            expense['Betrag'] = expense['Betrag'].lstrip('-')
            expenses.append(expense)
    return expenses


def get_incomes(file_data):
    incomes = []
    for income in file_data:
        if '-' not in income['Betrag']:
            incomes.append(income)
    return incomes


def visualise_data(input_data):
    labels = []
    sizes = []
    for entry in input_data:
        labels.append(entry['Auftraggeber/Empfänger'].strip())
        sizes.append(entry['Betrag'])
    y_pos = np.arange(len(labels))

    plt.barh(y_pos, sizes, align='center')
    plt.yticks(y_pos, labels)
    plt.xlabel('Values')
    # plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    # plt.axis('equal')
    plt.show()

parsed_file = parse(MY_FILE, ';')

# incomes = get_incomes(parsed_file)
# final_incomes = convert_decimal_values(incomes)

spendings = get_expenses(parsed_file)
converted_spendings = convert_decimal_values(spendings)
combine_rewe_spendings = sumup_rewe_spendings(converted_spendings)
combined_spendings = sumup_similar_spendings(combine_rewe_spendings)
final_data_spendings = remove_old_values(combined_spendings)

visualise_data(final_data_spendings)
# visualise_data(final_incomes)
