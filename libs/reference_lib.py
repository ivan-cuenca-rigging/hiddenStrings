# Imports
import logging

# Maya imports
from maya import cmds, mel

logging = logging.getLogger(__name__)


def get_reference_node(node):
    """
    Get the reference node

    Args:
        node (str): name of a node inside the reference

    Returns:
        str: reference node. E.G. 'referenceRN'.
    """
    return cmds.referenceQuery(node, referenceNode=True)


def get_reference_file(node):
    """
    Get the reference file path

    Args:
        node (str): name of a node inside the reference

    Returns:
        str: reference path
    """
    return cmds.referenceQuery(node, filename=True)


def reload_reference(node, *args):
    """
    Reload the reference

    Args:
        node (str): name of a node inside the reference. Defaults to None.

    Returns:
        str: reference path
    """
    if not node:
        node = cmds.ls(selection=True)[0]
        
    return cmds.file(get_reference_file(node=node), loadReference=get_reference_node(node=node))


def replace_reference(node, new_reference_path):
    """
    Replace a reference

    Args:
        node (str): name of a node inside the reference
        new_reference_path (str): path of the new reference

    Returns:
        str: reference path
    """
    return cmds.file(get_reference_file(node=node), loadReference=new_reference_path)


def replace_reference_window(node=None, *args):
    """
    Open the replace window

    Args:
        node (str): name of a node inside the reference. Defaults to None.
    """
    if not node:
        node = cmds.ls(selection=True)[0]

    mel.eval(f'replaceReference "{get_reference_file(node=node)}" "{get_reference_node(node=node)}"')


def load_reference_window(*args):
    """
    Open the load reference window
    """
    mel.eval('CreateReference')


def load_reference(reference_path):
    """
    Load a reference

    Args:
        reference_path (str): path of the reference

    Returns:
        str: reference path
    """
    return cmds.file(reference_path, reference=True, loadReference=True)


def remove_reference(node=None, *args):
    """
    Remove the reference

    Args:
        node (str): name of a node inside the reference. Defaults to None.
    """
    if not node:
        node = cmds.ls(selection=True)[0]
    
    reference_node = get_reference_node(node=node)
    reference_file = get_reference_file(node=node)

    cmds.file(removeReference=True, referenceNode=reference_node)
    logging.info(f'{reference_file} reference has been removed')
