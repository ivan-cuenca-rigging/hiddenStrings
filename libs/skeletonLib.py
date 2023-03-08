# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import skeletonHelper
from hiddenStrings.libs import sideLib, usageLib, mathLib


def set_joint_label(node, other_type_override=False):
    """
    set the joint's label
    :param node: str
    :param other_type_override: str
    """
    descriptor, side, usage = node.split('_')

    if side == sideLib.center:
        cmds.setAttr('{}.side'.format(node), 0)
    if side == sideLib.left:
        cmds.setAttr('{}.side'.format(node), 1)
    if side == sideLib.right:
        cmds.setAttr('{}.side'.format(node), 2)

    cmds.setAttr('{}.type'.format(node), 18)
    other_type_value = '{}{}'.format(descriptor, usage.capitalize())
    cmds.setAttr('{}.otherType'.format(node), other_type_value, type='string')
    if other_type_override:
        cmds.setAttr('{}.otherType'.format(node), other_type_override, type='string')


def set_joint_guide_label(node):
    set_joint_label(node=node, other_type_override=node)


def create_skeleton_hierarchy_from_a_to_b(descriptor, a, b,
                                          joints_number, joint_parent, joint_usage=usageLib.skin_joint):
    a_descriptor, a_side, a_usage = a.split('_')
    skin_joint_parent = joint_parent

    skin_start_mid_joint_point_list = mathLib.get_n_positions_from_a_to_b(a, b, joints_number)
    joint_list = list()
    for index in range(joints_number):
        joint_index = index + 1
        joint_usage = usageLib.joint if joint_index == joints_number else joint_usage
        skin_joint_sh = skeletonHelper.SkeletonHelper(name='{}{}_{}_{}'.format(descriptor,
                                                                               str(joint_index).zfill(2),
                                                                               a_side,
                                                                               joint_usage))
        skin_joint_sh.create(parent=skin_joint_parent)
        skin_joint_parent = skin_joint_sh.get_name()
        joint_list.append(skin_joint_sh.get_name())

        cmds.ToggleLocalRotationAxes(skin_joint_sh.get_name())

    # To avoid the automatic transform when the scale is != 1
    for index in range(joints_number):
        skin_joint_sh = skeletonHelper.SkeletonHelper(joint_list[index])
        if index == 0:
            skin_joint_sh.set_offset_parent_matrix(a)
        else:
            skin_joint_sh.set_position_from_point(skin_start_mid_joint_point_list[index])
            skin_joint_sh.set_rotation_from_point(a)

    return joint_list
