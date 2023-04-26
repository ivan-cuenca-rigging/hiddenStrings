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
    :param source_file: string
    :param destination_dir: string
    :param force: bool
    """
    destination_file = r'{}/{}'.format(destination_dir, source_file)

    if not os.path.exists(destination_dir):
        logging.info('could not create {}, please create the folder'.format(destination_dir))

    else:
        if not os.path.exists(destination_file):
            shutil.copy(source_file, destination_dir)
            logging.info('{} copied to {}'.format(source_file, destination_file))

        else:
            if force:
                shutil.copy(source_file, destination_dir)
                logging.info('{} copied to {}'.format(source_file, destination_file))


def copy_bifrost_compounds(source_dir, destination_dir, force=True):
    """
    Copy bifrost compounds from folder to folder
    :param source_dir: string
    :param destination_dir: string
    :param force: bool
    """
    compound_file_list = [x for x in os.listdir(source_dir) if x.endswith('.json')]

    if not os.path.exists(destination_dir):
        logging.info('could not create {}, please create the folder'.format(destination_dir))

    else:
        for compound_file in compound_file_list:
            source_file = r'{}/{}'.format(source_dir, compound_file)
            destination_file = r'{}/{}'.format(destination_dir, compound_file)

            if not os.path.exists(destination_file):
                shutil.copy(source_file, destination_dir)
                logging.info('{} copied to {}'.format(source_file, destination_file))

            else:
                if force:
                    shutil.copy(source_file, destination_dir)
                    logging.info('{} copied to {}'.format(source_file, destination_file))


def import_compound(compound_namespace, compound_name):
    """
    Import compound into maya scene
    :param compound_namespace: str
    :param compound_name: str
    """
    return mel.eval('bifrostGraph -importGraphAsShape "{}::{}"'.format(compound_namespace, compound_name))
