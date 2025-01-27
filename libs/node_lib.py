# Imports
import logging

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import side_lib, usage_lib, attribute_lib


logging = logging.getLogger(__name__)


class Helper(attribute_lib.Helper):
    """
    Node Helper class

    Args:
        name (str): name of the node
    """
    def __init__(self, name):
        """
        Initializes an instance of node Helper

        Args:
            name (str): name of the node
        """
        super(Helper, self).__init__(name)
        self.name = name
        self.name_tokens = self.name.split('_')
        self.descriptor, self.side, self.usage = self.name_tokens
        self.node_type = None

        self.check_tokens_len()
        self.check_side()
        self.check_node_type()


    # ---------- Checks Methods ----------
    def check_tokens_len(self):
        """
        Check if the name has 3 tokens {descriptor}_{side}_{usage}
        """
        if len(self.name_tokens) != 3:  # Check that the name has 3 tokens
            cmds.error('the name must have 3 tokens')


    def check_side(self):
        """
        Check if the name is in the side_lib
        """
        if self.side not in side_lib.valid_sides:
            cmds.error(f'the name must have a valid side, {side_lib.valid_sides}')


    def check_usage(self):
        """
        Check if the usage is a valid usage
        """
        if self.usage not in usage_lib.valid_usages:
            cmds.error(f'the name must have a valid usage, {usage_lib.valid_usages}')


    def check_node_type(self):
        """
        If the node exists, check the node type
        
        Returns:
            str: node type
        """
        if cmds.objExists(self.name):  # If exist get the node type
            self.node_type = cmds.nodeType(self.name)

        return self.node_type


    # ---------- Naming Methods ----------
    def get_name(self):
        """
        Get node's name
        
        Returns:
            str: name
        """
        return self.name


    def set_name(self, new_name):
        """
        Set node's name
        
        Args:
            new_name (str): new name
        """
        self.name = cmds.rename(self.name, new_name)


    def get_descriptor(self):
        """
        Get node's descriptor

        Returns:
            str: descriptor
        """
        return self.name_tokens[0]


    def get_descriptor_capitalize(self):
        """
        Get node's descriptor capitalize

        Returns:
            str: descriptor capitalize
        """
        return f'{self.get_descriptor()[0].upper()}{self.get_descriptor()[1:]}'


    def set_descriptor(self, new_descriptor):
        """
        Set node's descriptor

        Args:
            new_descriptor (str): new descriptor
        """
        self.name = cmds.rename(self.name, f'{new_descriptor}_{self.name_tokens[1]}_{self.name_tokens[2]}')


    def get_side(self):
        """
        Get node's side

        Returns:
            str: side
        """
        return self.name_tokens[1]


    def set_side(self, new_side):
        """
        Set node's side
        
        Args:
            new_side (str): new side
        """
        self.name = cmds.rename(self.name, f'{self.name_tokens[0]}_{new_side}_{self.name_tokens[2]}')


    def get_usage(self):
        """
        Get node's usage

        Returns:
            str: usage
        """
        return self.name_tokens[2]


    def get_usage_capitalize(self):
        """
        Get node's usage capitalize

        Returns:
            str: usage capitalize
        """
        return f'{self.get_usage()[0].upper()}{self.get_usage()[1:]}'


    def set_usage(self, new_usage):
        """
        set node's name
        
        Args:
            new_usage (str): new usage
        """
        self.name = cmds.rename(self.name, f'{self.name_tokens[0]}_{self.name_tokens[1]}_{new_usage}')


    def get_node_type(self):
        """
        Get the node type

        Returns:
            str: node type
        """
        return cmds.nodeType(self.name)


    # ---------- Position Methods ----------
    def set_to_zero(self):
        """
        Set transform and user defined attributes to default
        """
        ud_attrs_l = cmds.listAttr(self.name, ud=True, settable=True)
        for attr in ['translate', 'rotate', 'scale']:
            for axis in ['X', 'Y', 'Z']:
                if cmds.getAttr(f'{self.name}.{attr}{axis}', settable=True):
                    cmds.setAttr(f'{self.name}.{attr}{axis}', 0)
                    if attr == 'scale':
                        cmds.setAttr(f'{self.name}.{attr}{axis}', 1)
        if ud_attrs_l:
            for attr in ud_attrs_l:
                if cmds.getAttr(f'{self.name}.{attr}', settable=True):
                    if cmds.getAttr(f'{self.name}.{attr}', type=True) != 'string':
                        def_value = cmds.addAttr(f'{self.name}.{attr}', query=True, defaultValue=True)
                        cmds.setAttr(f'{self.name}.{attr}', def_value)
        if self.node_type == 'joint':
            for axis in ['X', 'Y', 'Z']:
                cmds.setAttr(f'{self.name}.jointOrient{axis}', 0)


    def get_matrix(self):
        """
        Get node's matrix

        Returns:
            matrix: node's matrix
        """
        return cmds.xform(self.name, query=True, worldSpace=True, matrix=True)


    def set_matrix(self, point):
        """
        Set node's matrix
        
        Args:
            point (str): point
        """
        point_matrix = cmds.xform(point, query=True, worldSpace=True, matrix=True)
        cmds.xform(self.name, worldSpace=True, matrix=point_matrix)


    def set_offset_parent_matrix(self, point, translation=False, rotation=False):
        """
        Set node's shape_offset parent matrix
        
        Args:
            point (str): point
            translation (bool): only translation. Defaults to False.
            rotation (bool): only rotation. Defaults to False.
        """
        if type(point) == list:
            point_matrix = point
        else:
            point_matrix = cmds.xform(point, query=True, worldSpace=True, matrix=True)

        if translation:
            node_matrix_rotation = cmds.xform(self.name, query=True, worldSpace=True, rotation=True)
            node_matrix_scale = cmds.xform(self.name, query=True, worldSpace=True, scale=True)
            ref_node = cmds.createNode('transform')
            cmds.xform(ref_node, worldSpace=True, matrix=point_matrix)
            cmds.xform(ref_node, worldSpace=True, rotation=node_matrix_rotation)
            cmds.xform(ref_node, worldSpace=True, scale=node_matrix_scale)
            point_matrix = cmds.xform(ref_node, query=True, worldSpace=True, matrix=True)
            cmds.delete(ref_node)

        if rotation:
            node_matrix_translation = cmds.xform(self.name, query=True, worldSpace=True, translation=True)
            node_matrix_scale = cmds.xform(self.name, query=True, worldSpace=True, scale=True)

            ref_node = cmds.createNode('transform')
            cmds.xform(ref_node, worldSpace=True, matrix=point_matrix)
            cmds.xform(ref_node, worldSpace=True, translation=node_matrix_translation)
            cmds.xform(ref_node, worldSpace=True, scale=node_matrix_scale)
            point_matrix = cmds.xform(ref_node, query=True, worldSpace=True, matrix=True)
            cmds.delete(ref_node)

        cmds.setAttr(f'{self.name}.offsetParentMatrix', point_matrix, type='matrix')


    def get_position(self):
        """
        Get node's position

        Returns:
            list: translate (x, y, z) values
        """
        return cmds.xform(self.name, query=True, worldSpace=True, translation=True)


    def set_position(self, x, y, z):
        """
        Set node's position

        Args:
            x (float): new x value
            y (float): new y value
            z (float): new z value
        """
        if x:
            cmds.setAttr(f'{self.name}.translateX', x)
        if y:
            cmds.setAttr(f'{self.name}.translateY', y)
        if z:
            cmds.setAttr(f'{self.name}.translateZ', z)


    def set_position_from_point(self, point):
        """
        Set node's position from point

        Args:
            point (str): point
        """
        if isinstance(point, list):
            point_position = point
        else:
            point_position = cmds.xform(point, query=True, worldSpace=True, translation=True)
        cmds.xform(self.name, worldSpace=True, translation=point_position)


    def get_rotation(self):
        """
        Get node's rotation

        Returns:
            list: rotation (x, y, z) values
        """
        return cmds.xform(self.name, query=True, worldSpace=True, rotation=True)


    def set_rotation(self, xyz=None, x=None, y=None, z=None):
        """
        Set node's rotation

        Args:
            xyz (float): new xyz value. Defaults to None.
            x (float): new x value. Defaults to None.
            y (float): new y value. Defaults to None.
            z (float): new z value. Defaults to None.
        """
        if xyz:
            for index, axis in enumerate('XYZ'):
                cmds.setAttr(f'{self.name}.rotate{axis}', xyz[index])
        if x:
            cmds.setAttr(f'{self.name}.rotateX', x)
        if y:
            cmds.setAttr(f'{self.name}.rotateY', y)
        if z:
            cmds.setAttr(f'{self.name}.rotateZ', z)


    def set_rotation_from_point(self, point):
        """
        Set node's rotation from point

        Args:
            point (str): point
        """
        point_rotation = cmds.xform(point, query=True, worldSpace=True, rotation=True)
        cmds.xform(self.name, worldSpace=True, rotation=point_rotation)


    def get_scale(self):
        """
        Get node's scale

        Returns:
            list: scale (x, y, z) values
        """
        return cmds.xform(self.name, query=True, worldSpace=True, scale=True)


    def set_scale(self, x, y, z):
        """
        Set node's scale

        Args:
            x (float): new x value
            y (float): new y value
            z (float): new z value
        """
        if x:
            cmds.setAttr(f'{self.name}.scaleX', x)
        if y:
            cmds.setAttr(f'{self.name}.scaleY', y)
        if z:
            cmds.setAttr(f'{self.name}.scaleZ', z)


    def set_scale_from_point(self, point):
        """
        Set node's scale from point

        Args:
            point (str): point
        """
        point_rotation = cmds.xform(point, query=True, worldSpace=True, scale=True)
        cmds.xform(self.name, worldSpace=True, scale=point_rotation)


    def aim_to(self, point, aim_vector='x', up_vector='z'):
        """
        Aim node's to the point
            point (str):
            aim_vector (str): 'x', 'y', 'z', '-x', '-y' or '-z'. Defaults to 'x'
            up_vector (str): 'x', 'y', 'z', '-x', '-y' or '-z'. Defaults to 'z'
        """
        vector_dict = {'x': (1, 0, 0),
                       'y': (0, 1, 0),
                       'z': (0, 0, 1),
                       '-x': (-1, 0, 0),
                       '-y': (0, -1, 0),
                       '-z': (0, 0, -1)
                       }
        aim_vector = vector_dict[aim_vector]
        up_vector = vector_dict[up_vector]
        if len(point) == 3:
            aim_to_ref = cmds.createNode('transform', name='temp')
            cmds.xform(aim_to_ref, worldSpace=True, translation=point)
            cmds.delete(cmds.aimConstraint(aim_to_ref, self.name, mo=False,
                                           aimVector=aim_vector, upVector=up_vector,
                                           worldUpType='vector',
                                           worldUpVector=up_vector))
            cmds.delete(aim_to_ref)

        else:
            cmds.delete(cmds.aimConstraint(point, self.name, mo=False,
                                        aimVector=aim_vector, upVector=up_vector,
                                        worldUpType='vector',
                                        worldUpVector=up_vector))


    # ---------- Hierarchy methods ----------
    def get_structural_parent(self):
        """
        Get node's parent

        Returns:
            str: structural parent
        """
        structural_parent = cmds.listRelatives(self.name, parent=True)
        if structural_parent:
            structural_parent = structural_parent[0]
        else:
            logging.info('It is a child of the parent "world".')
        return structural_parent


    def get_structural_parent_list(self):
        """
        Get node's parent list

        Returns:
            list: structural parent list
        """
        structural_parent_list = cmds.listRelatives(self.name, fullPath=True, parent=True)
        if structural_parent_list:
            structural_parent_list = structural_parent_list[0].split('|')[1::]

        return structural_parent_list


    def get_zero(self):
        """
        Get node's zero's name if it exists

        Returns:
            str: zero's name
        """
        zero = None
        zero_name = f'{self.get_descriptor()}{self.get_usage().capitalize()}_{self.get_side()}_zero'
        if cmds.objExists(zero_name):
            zero = zero_name
        return zero


    def create_zero(self):
        """
        Create an structural parent with the zero's usage

        Returns:
            str: zero name
        """
        return self.create_structural_parent(usage=usage_lib.zero)


    def create_structural_parent(self, usage):
        """
        Create structural parent
        
        Args:
            usage (str): usage

        Returns:
            str: structural parent
        """
        point_matrix = self.get_matrix()
        parent_name = f'{self.get_descriptor()}{self.get_usage().capitalize()}_{self.get_side()}_{usage}'
        if cmds.objExists(parent_name):
            new_structural_parent = parent_name
            logging.info('This parent already exists.')
        else:
            new_structural_parent = cmds.createNode('transform', name=parent_name, parent=self.get_structural_parent())
            self.set_to_zero()
            cmds.parent(self.name, new_structural_parent)
            cmds.xform(new_structural_parent, worldSpace=True, matrix=point_matrix)

        return new_structural_parent


    def set_parent(self, parent):
        """
        set node's parent

        Args:
            parent (str): parent name
        """
        if self.get_zero():
            cmds.parent(self.get_zero(), parent)
        else:
            cmds.parent(self.name, parent)
            if self.get_node_type() == 'joint':
                node_rotation = cmds.xform(self.name, query=True, worldSpace=True, rotation=True)
                for axis in 'XYZ':
                    cmds.setAttr(f'{self.name}.jointOrient{axis}', 0)
                cmds.xform(self.name, worldSpace=True, rotation=node_rotation)


    def set_parent_matrix(self, point):
        """
        Set node's parent's matrix

        Args:
            point (str): point
        """
        structural_parent = self.get_structural_parent()
        point_matrix = cmds.xform(point, query=True, worldSpace=True, matrix=True)
        cmds.xform(structural_parent, worldSpace=True, matrix=point_matrix)


    def set_parent_position(self, point):
        """
        set node's parent's position

        Args:
            point (str): point
        """
        structural_parent = self.get_structural_parent()
        if isinstance(point, str):
            point_matrix = cmds.xform(point, query=True, worldSpace=True, translation=True)
            cmds.xform(structural_parent, worldSpace=True, translation=point_matrix)
        else:
            cmds.xform(structural_parent, worldSpace=True, translation=point)


    def parent_aim_to(self, point, aim_vector='x', up_vector='z'):
        """
        Aim the node's parent to the point

        Args:
            point (str): point
            aim_vector (str): 'x', 'y', 'z', '-x', '-y' or '-z'. Defaults to 'x'
            up_vector (str): 'x', 'y', 'z', '-x', '-y' or '-z'. Defaults to 'z'
        """
        structural_parent = self.get_structural_parent()
        vector_dict = {'x': (1, 0, 0),
                       'y': (0, 1, 0),
                       'z': (0, 0, 1),
                       '-x': (-1, 0, 0),
                       '-y': (0, -1, 0),
                       '-z': (0, 0, -1)
                       }
        aim_vector = vector_dict[aim_vector]
        up_vector = vector_dict[up_vector]
        cmds.delete(cmds.aimConstraint(point, structural_parent, mo=False,
                                       aimVector=aim_vector, upVector=up_vector,
                                       worldUpType='vector',
                                       worldUpVector=up_vector))


    def __repr__(self):
        """
        Returns:
            str: name
        """
        return self.name
