# Imports
import json
import os


def export_data_to_json(data, file_name, file_path, relative_path=True, use_indent=True, compact=False):
    """
    export data to a json file
    :param data: str, list, dict
    :param file_name: str
    :param file_path: str
    :param relative_path: bool
    :param use_indent: bool
    :param compact: bool
    :return: file path name with ".json"
    """
    if relative_path:
        script_path = os.path.dirname(os.path.dirname(__file__))
        file_path_name_with_extension = '{}/{}/{}.json'.format(script_path, file_path, file_name)
    else:
        file_path_name_with_extension = '{}/{}.json'.format(file_path, file_name)

    if compact:
        with open(file_path_name_with_extension, 'w') as write_file:
            indent_value = 4 if use_indent else 0
            json.dump(data, write_file)
    else:
        with open(file_path_name_with_extension, 'w') as write_file:
            indent_value = 4 if use_indent else 0
            json.dump(data, write_file, indent=indent_value)

    return file_path_name_with_extension


def import_data_from_json(file_name, file_path, relative_path=True):
    """
    Import data from a json file
    :param file_name: str
    :param file_path: str
    :param relative_path: bool
    :return: data
    """
    if relative_path:
        script_path = os.path.dirname(os.path.dirname(__file__))
        file_path_name_with_extension = '{}/{}/{}.json'.format(script_path, file_path, file_name)
    else:
        file_path_name_with_extension = '{}/{}.json'.format(file_path, file_name)

    with open(file_path_name_with_extension, 'r') as read_file:
        data = json.load(read_file)

    return data


"""
from hiddenStrings.libs import jsonLib


# Export example
data_dict = dict()
data_dict['test'] = 'this is a test'

jsonLib.export_data_to_json(data=data_dict, file_name='test', file_path='libs/shapes')

# Import example
data_dict = (jsonLib.import_data_from_json(file_name='test', file_path='libs/shapes'))
"""