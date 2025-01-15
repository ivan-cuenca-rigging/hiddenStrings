# Imports
import logging

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import node_lib, side_lib, usage_lib, math_lib

logging = logging.getLogger(__name__)


class Helper(node_lib.Helper):
    """
    Skeleton Helper class

    Args:
        name (str): name of the joint
    """
    def __init__(self, name):
        """
        Initializes an instance of skeleton Helper

        Args:
            name (str): name of the joint
        """
        super(Helper, self).__init__(name)
        self.name = name
        self.check_usage()
        self.check_side()


    # ---------- Checks Methods----------
    def check_usage(self):
        """
        Check if the usage is valid
        """
        if self.get_usage() not in usage_lib.skeleton_valid_usages:
            logging.info('this control has not a valid usage, {}.'.format(usage_lib.skeleton_valid_usages))


    # ---------- Create Method ----------
    def create(self,
               zero=False,
               parent=None,
               matrix=None,
               matrix_translation=False,
               matrix_rotation=False):
        """
        Create a skeleton

        Args:
            zero (bool): if yes it will create a zero group. Defaults to False.
            parent (str): control's parent. Defaults to None.
            matrix (skeleton): control's matrix. Defaults to None.
            matrix_translation (bool): if true only translation will be used. Defaults to False.
            matrix_rotation (bool): if true only rotation will be used. Defaults to False.
        Returns:
            str: joint name
        """
        if cmds.objExists(self.name):
            cmds.error('the {} already exists in the scene'.format(self.name))

        cmds.createNode('joint', name=self.name)

        set_joint_label(self.name)

        if zero:
            self.create_zero()
        if parent:
            self.set_parent(parent)
        if matrix:
            self.set_offset_parent_matrix(matrix, translation=matrix_translation, rotation=matrix_rotation)

        cmds.select(self.name)

        return self.name


def set_joint_label(node, other_type_override=False):
    """
    Set the joint's label

    Args:
        node (str): node's name
        other_type_override (str): other type value. Defaults to False
    """
    descriptor, side, usage = node.split('_')

    if side == side_lib.center:
        cmds.setAttr('{}.side'.format(node), 0)
    if side == side_lib.left:
        cmds.setAttr('{}.side'.format(node), 1)
    if side == side_lib.right:
        cmds.setAttr('{}.side'.format(node), 2)

    cmds.setAttr('{}.type'.format(node), 18)
    other_type_value = '{}{}'.format(descriptor, usage.capitalize())
    cmds.setAttr('{}.otherType'.format(node), other_type_value, type='string')
    if other_type_override:
        cmds.setAttr('{}.otherType'.format(node), other_type_override, type='string')


def set_joint_guide_label(node):
    """
    Set the joint's guide label

    Args:
        node (str): node's name
    """
    set_joint_label(node=node, other_type_override=node)


def create_skeleton_chain_from_a_to_b(descriptor,
                                      a,
                                      b,
                                      joints_number,
                                      joint_parent,
                                      joint_usage=usage_lib.skin_joint):
    """
    Create a skeleton chain between two points

    Args:
        descriptor (str): descriptor
        a (str): node a
        b (str): node b
        joints_number (int): number of joints from a to b
        joint_parent (str): joint's parent
        joint_usage (str): joints usage
    
    Returns:
        list: joints list
    """
    a_descriptor, a_side, a_usage = a.split('_')
    skin_joint_parent = joint_parent

    skin_start_mid_joint_point_list = math_lib.get_n_positions_from_a_to_b(a, b, joints_number)
    joint_list = list()
    for index in range(joints_number):
        joint_index = index + 1
        joint_usage = usage_lib.joint if joint_index == joints_number else joint_usage
        skin_joint_sh = Helper(name='{}{}_{}_{}'.format(descriptor,
                                                        str(joint_index).zfill(2),
                                                        a_side,
                                                        joint_usage))
        skin_joint_sh.create(parent=skin_joint_parent)
        skin_joint_parent = skin_joint_sh.get_name()
        joint_list.append(skin_joint_sh.get_name())

    # To avoid the automatic transform when the scale is != 1
    for index in range(joints_number):
        skin_joint_sh = Helper(joint_list[index])
        if index == 0:
            skin_joint_sh.set_offset_parent_matrix(a)
        else:
            skin_joint_sh.set_position_from_point(skin_start_mid_joint_point_list[index])
            skin_joint_sh.set_rotation_from_point(a)

    return joint_list


def create_push_joint(parent_node, driver_node,
                      suffix='',
                      forbidden_word='01',
                      rotation_axis='Y',
                      structural_parent='pushJoints_c_grp'):
    """
    Create a pushJoint system

    Args:
        parent_node (str): base node
        driver_node (str): driver node
        suffix (str): suffix value. Defaults to ''.
        forbidden_word (str): if we want to avoid any word in the name. Defaults to '01'.
        rotation_axis (str): 'X', '-X', 'Y', '-Y', 'Z' or '-Z'Defaults to 'Y'.
        structural_parent (str): parent node. Defaults to 'pushJoints_c_grp'.
    """
    if len(parent_node.split('_')) == 3:
        parent_descriptor, parent_side, parent_usage = parent_node.split('_')
    else:
        parent_descriptor = parent_node
        parent_side = side_lib.center
        parent_usage = ''

    if len(driver_node.split('_')) == 3:
        descriptor, side, usage = driver_node.split('_')
    else:
        descriptor = driver_node
        side = side_lib.center

    push_attribute = 'pushValue'

    if forbidden_word:
        descriptor = ''.join(descriptor.split(forbidden_word))

    rotation_axis = rotation_axis.lower()
    if '-' in rotation_axis:
        rotation_axis = '{}M'.format(rotation_axis[-1])

    # driver matrix
    driver_mult_matrix = cmds.createNode('multMatrix', name='{}R{}Push{}_{}_{}'.format(parent_descriptor,
                                                                                       rotation_axis,
                                                                                       suffix,
                                                                                       parent_side,
                                                                                       usage_lib.mult_matrix))

    driven_matrix = cmds.getAttr('{}.worldMatrix'.format(driver_node))
    driver_inverse_matrix = cmds.getAttr('{}.worldInverseMatrix'.format(parent_node))
    matrix_difference = math_lib.multiply_matrices_4_by_4(driven_matrix, driver_inverse_matrix)
    cmds.setAttr('{}.matrixIn[0]'.format(driver_mult_matrix), matrix_difference, type='matrix')
    cmds.connectAttr('{}.worldMatrix'.format(parent_node), '{}.matrixIn[1]'.format(driver_mult_matrix))

    # BlendMatrix to get the position of the driver and half rotation from each
    blend_matrix = cmds.createNode('blendMatrix', name='{}R{}Push{}_{}_{}'.format(descriptor,
                                                                                  rotation_axis,
                                                                                  suffix,
                                                                                  side,
                                                                                  usage_lib.blend_matrix))

    cmds.connectAttr('{}.matrixSum'.format(driver_mult_matrix), '{}.inputMatrix'.format(blend_matrix))

    cmds.connectAttr('{}.worldMatrix'.format(driver_node), '{}.target[0].targetMatrix'.format(blend_matrix))
    cmds.setAttr('{}.target[0].translateWeight'.format(blend_matrix), 1)
    cmds.setAttr('{}.target[0].rotateWeight'.format(blend_matrix), 0.5)
    cmds.setAttr('{}.target[0].scaleWeight'.format(blend_matrix), 0)
    cmds.setAttr('{}.target[0].shearWeight'.format(blend_matrix), 0)

    # Zero the blend matrix rotation
    blend_mult_matrix = cmds.createNode('multMatrix', name='{}{}{}_{}_{}'.format(descriptor,
                                                                                 rotation_axis,
                                                                                 suffix,
                                                                                 side,
                                                                                 usage_lib.mult_matrix))

    cmds.setAttr('{}.matrixIn[0]'.format(blend_mult_matrix),
                 math_lib.inverse_matrix(matrix_a=cmds.getAttr('{}.outputMatrix'.format(blend_matrix))), type='matrix')
    cmds.connectAttr('{}.outputMatrix'.format(blend_matrix), '{}.matrixIn[1]'.format(blend_mult_matrix))

    # Decompose the matrix to get the rotation in 1 axis
    decompose_matrix = cmds.createNode('decomposeMatrix', name='{}R{}Push{}_{}_{}'.format(descriptor,
                                                                                          rotation_axis,
                                                                                          suffix,
                                                                                          side,
                                                                                          usage_lib.decompose_matrix))

    cmds.connectAttr('{}.matrixSum'.format(blend_mult_matrix), '{}.inputMatrix'.format(decompose_matrix))

    # Create structural parent if it does not exist
    if not cmds.objExists(structural_parent):
        cmds.createNode('transform', name=structural_parent)

    # PushJoint creation
    joint_sh = Helper(name='{}R{}Push{}_{}_{}'.format(descriptor,
                                                      rotation_axis,
                                                      suffix,
                                                      side,
                                                      usage_lib.skin_joint))
    joint_sh.create(parent=structural_parent)

    cmds.connectAttr('{}.outputMatrix'.format(blend_matrix), '{}.offsetParentMatrix'.format(joint_sh.get_name()))

    # Create attributes
    joint_sh.add_separator_attribute(separator_name='Attributes')
    joint_sh.add_float_attribute(attribute_name='{}X'.format(push_attribute))
    joint_sh.add_float_attribute(attribute_name='{}Y'.format(push_attribute))
    joint_sh.add_float_attribute(attribute_name='{}Z'.format(push_attribute))

    # Clamp push joint values
    push_clamp = cmds.createNode('clamp', name='{}R{}Push{}_{}_{}'.format(descriptor,
                                                                          rotation_axis,
                                                                          suffix,
                                                                          side,
                                                                          usage_lib.clamp))

    if 'M' in rotation_axis:
        cmds.setAttr('{}.minR'.format(push_clamp), -9999)
        cmds.setAttr('{}.minG'.format(push_clamp), -9999)
        cmds.setAttr('{}.minB'.format(push_clamp), -9999)

    else:
        cmds.setAttr('{}.maxR'.format(push_clamp), 9999)
        cmds.setAttr('{}.maxG'.format(push_clamp), 9999)
        cmds.setAttr('{}.maxB'.format(push_clamp), 9999)

    cmds.connectAttr('{}.outputRotateY'.format(decompose_matrix), '{}.inputR'.format(push_clamp))
    cmds.connectAttr('{}.outputRotateY'.format(decompose_matrix), '{}.inputG'.format(push_clamp))
    cmds.connectAttr('{}.outputRotateY'.format(decompose_matrix), '{}.inputB'.format(push_clamp))

    # Create multiplier connected to the attribute
    push_multiply = cmds.createNode('multiplyDivide', name='{}R{}Push{}_{}_{}'.format(descriptor,
                                                                                      rotation_axis,
                                                                                      suffix,
                                                                                      side,
                                                                                      usage_lib.multiply))

    cmds.connectAttr('{}.outputR'.format(push_clamp), '{}.input1X'.format(push_multiply))
    cmds.connectAttr('{}.outputG'.format(push_clamp), '{}.input1Y'.format(push_multiply))
    cmds.connectAttr('{}.outputB'.format(push_clamp), '{}.input1Z'.format(push_multiply))

    cmds.connectAttr('{}.{}'.format(joint_sh.get_name(), '{}X'.format(push_attribute)),
                     '{}.input2X'.format(push_multiply))
    cmds.connectAttr('{}.{}'.format(joint_sh.get_name(), '{}Y'.format(push_attribute)),
                     '{}.input2Y'.format(push_multiply))
    cmds.connectAttr('{}.{}'.format(joint_sh.get_name(), '{}Z'.format(push_attribute)),
                     '{}.input2Z'.format(push_multiply))

    cmds.connectAttr('{}.outputX'.format(push_multiply), '{}.translateX'.format(joint_sh.get_name()))
    cmds.connectAttr('{}.outputY'.format(push_multiply), '{}.translateY'.format(joint_sh.get_name()))
    cmds.connectAttr('{}.outputZ'.format(push_multiply), '{}.translateZ'.format(joint_sh.get_name()))

    # Lock attributes
    joint_sh.lock_and_hide_attributes(attributes_list=['translateX', 'translateY', 'translateZ',
                                                       'rotateX', 'rotateY', 'rotateZ',
                                                       'scaleX', 'scaleY', 'scaleZ',
                                                       'visibility', 'radius'])

    return joint_sh.get_name()


def create_local_skeleton(skeleton_grp,
                          world_control='center_c_ctr'):
    """
    Create a local joint for each skeleton joint

    Args:
        skeleton_grp (str): skeleton group
        world_control (str): world base control. Defaults to 'center_c_ctr'.
    Returns:
        list: local joints list
    """
    if cmds.listRelatives(skeleton_grp, allDescendents=True):
        skeleton_group_nh = node_lib.Helper(skeleton_grp)

        skeleton_local_grp = cmds.createNode('transform', name='{}Local_{}_{}'.format(skeleton_group_nh.get_descriptor(),
                                                                                      skeleton_group_nh.get_side(),
                                                                                      usage_lib.group))
        cmds.parent(skeleton_local_grp, skeleton_group_nh.get_structural_parent())

        skeleton_joint_list = [x for x in cmds.listRelatives(skeleton_grp, children=True, allDescendents=True) if
                               x.endswith(usage_lib.skin_joint)]
        local_joint_list = list()
        for skin_joint in skeleton_joint_list:
            skin_joint_helper = Helper(skin_joint)
            skin_joint_local = cmds.createNode('joint', name='{}Local_{}_{}'.format(skin_joint_helper.get_descriptor(),
                                                                                    skin_joint_helper.get_side(),
                                                                                    skin_joint_helper.get_usage()))
            local_joint_list.append(skin_joint_local)

            cmds.parent(skin_joint_local, skeleton_local_grp)

            mult_mat = cmds.createNode('multMatrix', name='{}Local_{}_{}'.format(skin_joint_helper.get_descriptor(),
                                                                                 skin_joint_helper.get_side(),
                                                                                 usage_lib.mult_matrix))

            cmds.connectAttr('{}.worldMatrix'.format(skin_joint), '{}.matrixIn[0]'.format(mult_mat))
            cmds.connectAttr('{}.worldInverseMatrix'.format(world_control), '{}.matrixIn[1]'.format(mult_mat))

            cmds.connectAttr('{}.matrixSum'.format(mult_mat), '{}.offsetParentMatrix'.format(skin_joint_local))

        return local_joint_list


def show_skeleton(*args):
    skeleton_grp_list = cmds.ls('*_*_{}'.format(usage_lib.skeleton))
    if skeleton_grp_list:
        for grp in skeleton_grp_list:
            try:
                cmds.setAttr('{}.visibility'.format(grp), 1)
            except:
                logging.info('{} visibility is locked or connected'.format(grp))


def hide_skeleton(*args):
    skeleton_grp_list = cmds.ls('*_*_{}'.format(usage_lib.skeleton))
    if skeleton_grp_list:
        for grp in skeleton_grp_list:
            try:
                cmds.setAttr('{}.visibility'.format(grp), 0)
            except:
                logging.info(
                    '{} visibility is locked or connected'.format(grp))
