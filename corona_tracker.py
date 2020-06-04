"""
    @author: Shivam Chauhan | @chashiv
    @Date: June 5, 2020
    @about_this_code:
        Prepares hot 'n' sour soup ;-) containing coronavirus updates from the
        government's website and __hook up__ the details to the desired 'Slack Channel'
"""

from bs4 import BeautifulSoup
from utils import get_delta_dict, get_data_dict
from pydash import is_empty
import requests
import csv
import constants
from secrets import workspace_file_path


# -------------------------------------- CONSTANTS -------------------------------------------

# An array to hold the value of cells in the grid
current_reader, past_reader = [], []

file_path = workspace_file_path

# -------------------------------------- CONSTANTS -------------------------------------------


# Preparing the tastiest soup
response = requests.get(constants.URL).content
soup = BeautifulSoup(response, 'html.parser')

rows = soup.find_all('tr')


def delta_evaluator():
    """
    Evaluates the delta based on past and current data, if the changes occur in each state
    corresponding message is added against them
    :return:
    """
    global past_reader, current_reader
    past_reader = list(csv.reader(open(file_path, 'r')))
    past_data, current_data = get_data_dict(past_reader), get_data_dict(current_reader)
    delta_dict = get_delta_dict(past_data, current_data)
    for index, msg in delta_dict.items():
        current_reader[index][constants.UPDATED_HIGHLIGHTER_INDEX] = " | ".join(msg)

    return not is_empty(delta_dict)


def corona_details_extractor():
    """
    Extracts the details of the corona and inserts them into the reader
    :return:
    """
    global current_reader

    for index, row in enumerate(rows):
        row_to_be_inserted = []

        # inserting the headers at row numbered 0
        if not index:
            current_reader.insert(index, constants.HEADERS)
            continue

        # forming the each row
        for column in row.find_all('td'):
            # extracting the text from columns parsed via soup
            row_to_be_inserted.append(
                column.text.replace(constants.NEW_LINE_CHARACTER, '')
            )

        # adding the row to the reader array
        if len(row_to_be_inserted):
            # adding the column with the value '' under the header Updated Highlighter
            row_to_be_inserted.append('')
            current_reader.insert(index, row_to_be_inserted)


if __name__ == '__main__':
    corona_details_extractor()

    delta_exists = delta_evaluator()

    file = open(file_path, 'w')
    writer = csv.writer(file)
    writer.writerows(current_reader)
    file.close()

    if delta_exists:
        import slack_client
