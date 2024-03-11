# Imports
import logging

# Maya imports
from maya import cmds

logging = logging.getLogger(__name__)


class Helper(object):
    """
    attribute Helper class

    Args:
        name (str): name of the node
    """
    def __init__(self, name):
        """
        Initializes an instance of attribute's Helper

        Args:
            name (str): name of the node
        """
        self.name = name

    # ---------- Checks Methods ----------
    def check_attribute_exists(self, attribute_name):
        """
        Check if the attribute's name exists in the node

        Args:
            attribute_name (str): name of the attribute

        Returns:
            bool: True if the attribute exist
        """
        if cmds.attributeQuery(attribute_name, node=self.name, exists=True):
            return True
        else:
            return False

    # ---------- Set methods ----------
    def lock_attribute(self, attribute_name, lock=True):
        """
        Lock the attribute given

        Args:
            attribute_name (str): name of the attribute
            lock (bool, optional): True == lock. Defaults to True.
        """
        if cmds.getAttr('{}.{}'.format(self.name, attribute_name), settable=True):
            cmds.setAttr('{}.{}'.format(self.name, attribute_name), lock=lock)

    def lock_attributes(self, attributes_list, lock=True):
        """
        Lock a list of the attributes given

        Args:
            attributes_list (list): list of attributes to lock
            lock (bool, optional): True == lock. Defaults to True.
        """
        for attr in attributes_list:
            self.lock_attribute(attr, lock=lock)

    def hide_attribute(self, attribute_name, hide=True):
        """
        Hide the attribute given

        Args:
            attribute_name (str): name of the attribute
            hide (bool, optional): True == hide. Defaults to True.
        """
        cmds.setAttr('{}.{}'.format(self.name, attribute_name), keyable=not hide, channelBox=not hide)

    def hide_attributes(self, attributes_list, hide=True):
        """
        hide a list of the attributes given

        Args:
            attributes_list (list): list of attributes to hide
            hide (bool, optional): True == hide. Defaults to True.
        """
        for attr in attributes_list:
            self.hide_attribute(attr, hide=hide)

    def lock_and_hide_attribute(self, attribute_name, lock=True, hide=True):
        """
        Lock and hide the attribute given

        Args:
            attribute_name (str): name of the attribute
            lock (bool, optional): True == lock. Defaults to True.
            hide (bool, optional): True == hide. Defaults to True.
        """
        self.lock_attribute(attribute_name, lock)
        self.hide_attribute(attribute_name, hide)

    def lock_and_hide_attributes(self, attributes_list, lock=True, hide=True):
        """
        Lock and hide a list of the attributes given

        Args:
            attributes_list (list): list of attributes to lock and hide
            lock (bool, optional): True == lock. Defaults to True.
            hide (bool, optional): True == hide. Defaults to True.
        """
        for attr in attributes_list:
            self.lock_and_hide_attribute(attr, lock, hide)

    def keyable_attribute(self, attribute_name, keyable=True):
        """
        Change the attribute property between keyable and not keyable

        Args:
            attribute_name (str): name of the attribute
            keyable (bool, optional): True == keyable. Defaults to True.
        """
        cmds.setAttr('{}.{}'.format(self.name, attribute_name), keyable=keyable, channelBox=not keyable)

    def set_default_value(self, attr, value):
        cmds.addAttr('{}.{}'.format(self.name, attr), edit=True, defaultValue=value)
        cmds.setAttr('{}.{}'.format(self.name, attr), value)

    # ---------- Add attributes Methods ----------
    def add_attribute(self, attribute_name, keyable=True, **kwargs):
        """
        Add an attribute to the node

        Args:
            attribute_name (str): name of the new attribute
            keyable (bool, optional): True == keyable. Defaults to True.

        Returns:
            str: name of the attribute
        """
        if self.check_attribute_exists(attribute_name):
            logging.info('{}.{} already exists.'.format(self.name, attribute_name))
        else:
            cmds.addAttr(self.name, longName=attribute_name, **kwargs)
            cmds.setAttr('{}.{}'.format(self.name, attribute_name), keyable=keyable, channelBox=not keyable)

        return attribute_name

    def add_separator_attribute(self, separator_name):
        """
        Add a separator in the attribute list

        Args:
            separator_name (str): name of the separator

        Returns:
            str: name of the separator
        """
        if not cmds.attributeQuery(separator_name, node=self.name, exists=True):
            self.add_attribute(separator_name, niceName=' ', attributeType='enum',
                               enumName=separator_name)
            self.keyable_attribute(separator_name, keyable=False)
            self.lock_attribute(separator_name)

        return separator_name

    def add_float_attribute(self, attribute_name, keyable=True, **kwargs):
        """
        Add a float attribute

        Args:
            attribute_name (str): name of the attribute
            keyable (bool, optional): True == keyable. Defaults to True.

        Returns:
            str: name of the attribute
        """
        return self.add_attribute(attribute_name, attributeType='float', keyable=keyable, **kwargs)

    def add_int_attribute(self, attribute_name, keyable=True, **kwargs):
        """
        Add an int attribute

        Args:
            attribute_name (str): name of the attribute
            keyable (bool, optional): True == keyable. Defaults to True.

        Returns:
            str: name of the attribute
        """
        return self.add_attribute(attribute_name, attributeType='long', keyable=keyable, **kwargs)

    def add_bool_attribute(self, attribute_name, keyable=True, **kwargs):
        """
        Add a bool attribute

        Args:
            attribute_name (str): name of the attribute
            keyable (bool, optional): True == keyable. Defaults to True.

        Returns:
            str: name of the attribute
        """
        return self.add_attribute(attribute_name, attributeType='bool', keyable=keyable, **kwargs)

    def add_enum_attribute(self, attribute_name, states, keyable=True, **kwargs):
        """
        Add an enum attribute
        :param states: str, separate the values with ":"
        :param attribute_name: str
        :param keyable: bool
        :param kwargs: minValue, maxValue, defaultValue, etc
        :return: attribute's name

        Args:
            attribute_name (str): name of the attribute
            states (str): separate the values with ':'. E.G. 'high:low'.
            keyable (bool, optional): True == keyable. Defaults to True.

        Returns:
            str: name of the attribute
        """
        return self.add_attribute(attribute_name, attributeType='enum', enumName=states, keyable=keyable, **kwargs)

    def add_proxy_attribute(self, attribute_name, node_attribute_proxy):
        """
        Args:
            attribute_name (str): name of the attribute
            node_attribute_proxy (str): E.G. 'node.attribute'

        Returns:
            str: name of the attribute
        """
        cmds.addAttr(self.name, longName=attribute_name, proxy=node_attribute_proxy)

        return attribute_name

    def add_matrix_attribute(self, attribute_name, **kwargs):
        """
        Add a matrix attribute

        Args:
            attribute_name (str): name of the attribute

        Returns:
            str: name of the attribute
        """
        return self.add_attribute(attribute_name, attributeType='matrix', **kwargs)

    def add_string_attribute(self, attribute_name, text):
        """
        Add a string attribute

        Args:
            attribute_name (str): name of the attribute
            text (str): text inside of the string attribute

        Returns:
            str: name of the attribute
        """
        self.add_attribute(attribute_name, dataType='string')
        cmds.setAttr('{}.{}'.format(self.name, attribute_name), text, type='string')
        return attribute_name

    # ---------- Get attributes Methods ----------
    def get_user_defined_attributes(self):
        """
        Get the user defined attributes

        Returns:
            list: list of attributes
        """
        return cmds.listAttr(self.name, userDefined=True, settable=True)
