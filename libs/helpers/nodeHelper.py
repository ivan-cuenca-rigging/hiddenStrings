# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import sideLib
from hiddenStrings.libs import usageLib

from hiddenStrings.libs.helpers import attributeHelper


class NodeHelper(attributeHelper.AttributeHelper):
    def __init__(self, name):
        """
        :param name: str
        """
        super(NodeHelper, self).__init__(name)
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
        check if the name has 3 tokens {descriptor}_{side}_{usage}
        """
        if len(self.name_tokens) != 3:  # Check that the name has 3 tokens
            cmds.error('the name must have 3 tokens')

    def check_side(self):
        """
        Check if the name is in the sideLib
        """
        if self.side not in sideLib.valid_sides:
            cmds.error('the name must have a valid side, {}'.format(sideLib.valid_sides))

    def check_usage(self):
        """
        Check if the usage is a valid usage
        """
        if self.usage not in usageLib.valid_usages:
            cmds.error('the name must have a valid usage, {}'.format(usageLib.valid_usages))

    def check_node_type(self):
        """
        if the node exists, check the node type
        :return: node type
        """
        if cmds.objExists(self.name):  # If exist get the node type
            self.node_type = cmds.nodeType(self.name)

        return self.node_type

    # ---------- Naming Methods ----------
    def get_name(self):
        """
        Get node's name
        :return: name
        """
        return self.name

    def set_name(self, new_name):
        """
        Set node's name
        :param new_name: str
        """
        self.name = cmds.rename(self.name, new_name)

    def get_descriptor(self):
        """
        Get node's descriptor
        :return: descriptor
        """
        return self.name_tokens[0]

    def get_descriptor_capitalize(self):
        """
        Get node's descriptor capitalize
        :return: descriptor capitalize
        """
        return '{}{}'.format(self.get_descriptor()[0].upper(), self.get_descriptor()[1:])

    def set_descriptor(self, new_descriptor):
        """
        Set node's descriptor
        :param new_descriptor: str
        """
        self.name = cmds.rename(self.name, '{}_{}_{}'.format(new_descriptor, self.name_tokens[1], self.name_tokens[2]))

    def get_side(self):
        """
        Get node's side
        :return: side
        """
        return self.name_tokens[1]

    def set_side(self, new_side):
        """
        Set node's side
        :param new_side: str
        """
        self.name = cmds.rename(self.name, '{}_{}_{}'.format(self.name_tokens[0], new_side, self.name_tokens[2]))

    def get_usage(self):
        """
        Get node's usage
        :return: usage
        """
        return self.name_tokens[2]

    def get_usage_capitalize(self):
        """
        Get node's usage capitalize
        :return: usage capitalize
        """
        return '{}{}'.format(self.get_usage()[0].upper(), self.get_usage()[1:])

    def set_usage(self, new_usage):
        """
        set node's name
        :param new_usage: str
        """
        self.name = cmds.rename(self.name, '{}_{}_{}'.format(self.name_tokens[0], self.name_tokens[1], new_usage))

    def get_node_type(self):
        return cmds.nodeType(self.name)

    # ---------- Position Methods ----------
    def set_to_zero(self):
        """
        set transform and user defined attributes to default
        """
        ud_attrs_l = cmds.listAttr(self.name, ud=True, settable=True)
        for attr in ['translate', 'rotate', 'scale']:
            for axis in ['X', 'Y', 'Z']:
                if cmds.getAttr('{}.{}{}'.format(self.name, attr, axis), settable=True):
                    cmds.setAttr('{}.{}{}'.format(self.name, attr, axis), 0)
                    if attr == 'scale':
                        cmds.setAttr('{}.{}{}'.format(self.name, attr, axis), 1)
        if ud_attrs_l:
            for attr in ud_attrs_l:
                if cmds.getAttr('{}.{}'.format(self.name, attr), settable=True):
                    if cmds.getAttr('{}.{}'.format(self.name, attr), type=True) != 'string':
                        def_value = cmds.addAttr('{}.{}'.format(self.name, attr), query=True, defaultValue=True)
                        cmds.setAttr('{}.{}'.format(self.name, attr), def_value)
        if self.node_type == 'joint':
            for axis in ['X', 'Y', 'Z']:
                cmds.setAttr('{}.jointOrient{}'.format(self.name, axis), 0)

    def get_matrix(self):
        """
        Get node's matrix
        :return: matrix
        """
        return cmds.xform(self.name, query=True, worldSpace=True, matrix=True)

    def set_matrix(self, point):
        """
        Set node's matrix
        :param point: str
        """
        point_matrix = cmds.xform(point, query=True, worldSpace=True, matrix=True)
        cmds.xform(self.name, worldSpace=True, matrix=point_matrix)

    def set_offset_parent_matrix(self, point, translation=False, rotation=False):
        """
        Set node's shape_offset parent matrix
        :param point: str
        :param translation: bool
        :param rotation: bool
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

        cmds.setAttr('{}.offsetParentMatrix'.format(self.name), point_matrix, type='matrix')

    def get_position(self):
        """
        Get node's position
        :return: translate values
        """
        return cmds.xform(self.name, query=True, worldSpace=True, translation=True)

    def set_position(self, x, y, z):
        """
        Set node's position
        :param x: float
        :param y: float
        :param z: float
        """
        if x:
            cmds.setAttr('{}.translateX'.format(self.name), x)
        if y:
            cmds.setAttr('{}.translateY'.format(self.name), y)
        if z:
            cmds.setAttr('{}.translateZ'.format(self.name), z)

    def set_position_from_point(self, point):
        """
        Set node's position from point
        :param point: str
        """
        if isinstance(point, list):
            point_position = point
        else:
            point_position = cmds.xform(point, query=True, worldSpace=True, translation=True)
        cmds.xform(self.name, worldSpace=True, translation=point_position)

    def get_rotation(self):
        """
        Get node's rotation
        :return: rotation values
        """
        return cmds.xform(self.name, query=True, worldSpace=True, rotation=True)

    def set_rotation(self, xyz=None, x=None, y=None, z=None):
        """
        Set node's rotation
        :param xyz: float
        :param x: float
        :param y: float
        :param z: float
        """
        if xyz:
            for index, axis in enumerate('XYZ'):
                cmds.setAttr('{}.rotate{}'.format(self.name, axis), xyz[index])
        if x:
            cmds.setAttr('{}.rotateX'.format(self.name), x)
        if y:
            cmds.setAttr('{}.rotateY'.format(self.name), y)
        if z:
            cmds.setAttr('{}.rotateZ'.format(self.name), z)

    def set_rotation_from_point(self, point):
        """
        Set node's rotation from point
        :param point: str
        """
        point_rotation = cmds.xform(point, query=True, worldSpace=True, rotation=True)
        cmds.xform(self.name, worldSpace=True, rotation=point_rotation)

    def get_scale(self):
        """
        Get node's scale
        :return: scale values
        """
        return cmds.xform(self.name, query=True, worldSpace=True, scale=True)

    def set_scale(self, x, y, z):
        """
        Set node's scale
        :param x: float
        :param y: float
        :param z: float
        """
        if x:
            cmds.setAttr('{}.scaleX'.format(self.name), x)
        if y:
            cmds.setAttr('{}.scaleY'.format(self.name), y)
        if z:
            cmds.setAttr('{}.scaleZ'.format(self.name), z)

    def set_scale_from_point(self, point):
        """
        Set node's scale from point
        :param point: str
        """
        point_rotation = cmds.xform(point, query=True, worldSpace=True, scale=True)
        cmds.xform(self.name, worldSpace=True, scale=point_rotation)

    def aim_to(self, point, aim_vector='x', up_vector='z'):
        """
        Aim node's to the point
        :param point: str
        :param aim_vector: str, 'x', 'y', 'z', '-x', '-y' or '-z'
        :param up_vector: str, 'x', 'y', 'z', '-x', '-y' or '-z'
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
        cmds.delete(cmds.aimConstraint(point, self.name, mo=False,
                                       aimVector=aim_vector, upVector=up_vector,
                                       worldUpType='vector',
                                       worldUpVector=up_vector))

    # ---------- Hierarchy methods ----------
    def get_structural_parent(self):
        """
        Get node's parent
        :return: structural parent
        """
        structural_parent = cmds.listRelatives(self.name, parent=True)
        if structural_parent:
            structural_parent = structural_parent[0]
        else:
            print('It is a child of the parent, "world".')
        return structural_parent

    def get_structural_parent_list(self):
        """
        Get node's parent list
        :return: structural parent list
        """
        structural_parent_list = cmds.listRelatives(self.name, fullPath=True, parent=True)
        if structural_parent_list:
            structural_parent_list = structural_parent_list[0].split('|')[1::]

        return structural_parent_list

    def get_zero(self):
        """
        Get node's zero's name if it exists
        :return: zero's name
        """
        zero = None
        zero_name = '{}{}_{}_zero'.format(self.get_descriptor(), self.get_usage().capitalize(), self.get_side())
        if cmds.objExists(zero_name):
            zero = zero_name
        return zero

    def create_zero(self):
        """
        Create an structural parent with the zero's usage
        :return:
        """
        return self.create_structural_parent(usage=usageLib.zero)

    def create_structural_parent(self, usage):
        """
        Create structural parent
        :param usage: str
        :return: structural parent
        """
        point_matrix = self.get_matrix()
        parent_name = '{}{}_{}_{}'.format(self.get_descriptor(), self.get_usage().capitalize(), self.get_side(), usage)
        if cmds.objExists(parent_name):
            new_structural_parent = parent_name
            cmds.warning('This parent already exists')
        else:
            new_structural_parent = cmds.createNode('transform', name=parent_name, parent=self.get_structural_parent())
            self.set_to_zero()
            cmds.parent(self.name, new_structural_parent)
            cmds.xform(new_structural_parent, worldSpace=True, matrix=point_matrix)

        return new_structural_parent

    def set_parent(self, parent):
        """
        set node's parent
        :param parent: str
        """
        if self.get_zero():
            cmds.parent(self.get_zero(), parent)
        else:
            cmds.parent(self.name, parent)
            if self.get_node_type() == 'joint':
                node_rotation = cmds.xform(self.name, query=True, worldSpace=True, rotation=True)
                for axis in 'XYZ':
                    cmds.setAttr('{}.jointOrient{}'.format(self.name, axis), 0)
                cmds.xform(self.name, worldSpace=True, rotation=node_rotation)

    def set_parent_matrix(self, point):
        """
        Set node's parent's matrix
        :param point: str
        """
        structural_parent = self.get_structural_parent()
        point_matrix = cmds.xform(point, query=True, worldSpace=True, matrix=True)
        cmds.xform(structural_parent, worldSpace=True, matrix=point_matrix)

    def set_parent_position(self, point):
        """
        set node's parent's position
        :param point: str
        """
        structural_parent = self.get_structural_parent()
        if isinstance(point, str):
            point_matrix = cmds.xform(point, query=True, worldSpace=True, translation=True)
            cmds.xform(structural_parent, worldSpace=True, translation=point_matrix)
        else:
            cmds.xform(structural_parent, worldSpace=True, translation=point)

    def parent_aim_to(self,  point, aim_vector='x', up_vector='z'):
        """
        Aim the node's parent to the point
        :param point: str
        :param aim_vector: str, 'x', 'y', 'z', '-x', '-y' or '-z'
        :param up_vector: str, 'x', 'y', 'z', '-x', '-y' or '-z'
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
        :return: name
        """
        return self.name
