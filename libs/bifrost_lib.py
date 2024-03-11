# Imports
import os
import shutil
import logging

# Maya imports
from maya import mel

# Project imports
from hiddenStrings import module_utils

logging = logging.getLogger(__name__)

bifrost_path = r'{}/autodesk/Bifrost/compounds'.format(os.path.dirname(
                                                        os.path.dirname(
                                                          os.path.dirname(
                                                            os.path.dirname(
                                                              os.path.dirname(module_utils.hidden_strings_path))))))


def copy_bifrost_compound(source_file, destination_dir, force=True):
    """
    Copy bifrost compounds from folder to folder

    Args:
        source_file (str): source file path
        destination_dir (str): destination folder path
        force (bool, optional): if the file is protected it will force it. Defaults to True.
    """
    destination_file = r'{}/{}'.format(destination_dir, source_file)

    if not os.path.exists(destination_dir):
        logging.info('could not create {}, please create the folder.'.format(destination_dir))

    else:
        if not os.path.exists(destination_file):
            shutil.copy(source_file, destination_dir)
            logging.info('{} copied to {}.'.format(source_file, destination_file))

        else:
            if force:
                shutil.copy(source_file, destination_dir)
                logging.info('{} copied to {}.'.format(source_file, destination_file))


def copy_bifrost_compounds(source_dir, destination_dir, force=True):
    """
    Copy bifrost compounds from folder to folder

    Args:
        source_dir (str): source folder path
        destination_dir (str): destination folder path
        force (bool, optional): if the files are protected it will force them. Defaults to True.
    """
    compound_file_list = [x for x in os.listdir(source_dir) if x.endswith('.json')]

    if not os.path.exists(destination_dir):
        logging.info('could not create {}, please create the folder.'.format(destination_dir))

    else:
        for compound_file in compound_file_list:
            source_file = r'{}/{}'.format(source_dir, compound_file)
            destination_file = r'{}/{}'.format(destination_dir, compound_file)

            if not os.path.exists(destination_file):
                shutil.copy(source_file, destination_dir)
                logging.info('{} copied to {}.'.format(source_file, destination_file))

            else:
                if force:
                    shutil.copy(source_file, destination_dir)
                    logging.info('{} copied to {}.'.format(source_file, destination_file))


def import_compound(compound_namespace, compound_name):
    """
    Import compound into maya scene

    Args:
        compound_namespace (str): name of the namespace
        compound_name (str): name of the compound

    Returns:
        str: name of the bifrost node imported
    """
    return mel.eval('bifrostGraph -importGraphAsShape "{}::{}"'.format(compound_namespace, compound_name))
