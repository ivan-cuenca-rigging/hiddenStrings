# Imports
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import jsonLib


store_selection_data_file_name = 'storeSelection_data'
store_selection_path = r'{}\temp'.format(os.path.dirname(os.path.dirname(__file__)))

if not os.path.exists(store_selection_path):
    os.makedirs(store_selection_path)


def save_selection(*args):
    selection_data = cmds.ls(selection=True)

    jsonLib.export_data_to_json(data=selection_data, file_name=store_selection_data_file_name,
                                file_path=store_selection_path, relative_path=False)
    return selection_data


def load_selection(*args):
    store_selection_data = jsonLib.import_data_from_json(file_name=store_selection_data_file_name,
                                                         file_path=store_selection_path, relative_path=False)

    cmds.select(store_selection_data)
    return store_selection_data
