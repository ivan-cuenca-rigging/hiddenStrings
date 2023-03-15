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
    """
    set the joint's guide label
    :param node: str
    """
    set_joint_label(node=node, other_type_override=node)


def create_skeleton_chain_from_a_to_b(descriptor,
                                      a,
                                      b,
                                      joints_number,
                                      joint_parent,
                                      joint_usage=usageLib.skin_joint):
    """
    Create a skeleton chain between two points
    :param descriptor: str
    :param a: str
    :param b: str
    :param joints_number: int
    :param joint_parent: str
    :param joint_usage: str
    return joint chain list
    """
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


def push_joint(parent_node, driven_node,
               suffix='',
               forbidden_word='01',
               rotation_axis='Y',
               structural_parent='pushJoints_c_grp'):
    """
    Create a pushJoint system
    :param parent_node: str
    :param driven_node: str
    :param suffix: str
    :param forbidden_word: str
    :param rotation_axis: str; X, -X, Y, -Y, Z or -Z
    :param structural_parent: str
    """
    if len(driven_node.split('_')) == 3:
        descriptor, side, usage = driven_node.split('_')
    else:
        descriptor = driven_node
        side = sideLib.center

    push_attribute = 'pushValue'

    if forbidden_word:
        descriptor = ''.join(descriptor.split(forbidden_word))

    rotation_axis = rotation_axis.lower()
    if '-' in rotation_axis:
        rotation_axis = '{}M'.format(rotation_axis[-1])

    # BlendMatrix to get the position of the driver and half rotation from each
    blend_matrix = cmds.createNode('blendMatrix', name='{}R{}Push{}_{}_{}'.format(descriptor,
                                                                                  rotation_axis,
                                                                                  suffix,
                                                                                  side,
                                                                                  usageLib.blend_matrix))

    cmds.connectAttr('{}.worldMatrix'.format(parent_node), '{}.inputMatrix'.format(blend_matrix))
    cmds.connectAttr('{}.worldMatrix'.format(driven_node), '{}.target[0].targetMatrix'.format(blend_matrix))

    cmds.setAttr('{}.target[0].translateWeight'.format(blend_matrix), 1)
    cmds.setAttr('{}.target[0].rotateWeight'.format(blend_matrix), 0.5)
    cmds.setAttr('{}.target[0].scaleWeight'.format(blend_matrix), 0)
    cmds.setAttr('{}.target[0].shearWeight'.format(blend_matrix), 0)

    # Decompose the matrix to get the rotation in 1 axis
    decompose_matrix = cmds.createNode('decomposeMatrix', name='{}R{}Push{}_{}_{}'.format(descriptor,
                                                                                          rotation_axis,
                                                                                          suffix,
                                                                                          side,
                                                                                          usageLib.decompose_matrix))
    cmds.connectAttr('{}.outputMatrix'.format(blend_matrix), '{}.inputMatrix'.format(decompose_matrix))

    # Create structural parent if it does not exist
    if not cmds.objExists(structural_parent):
        cmds.createNode('transform', name=structural_parent)

    # PushJoint creation
    joint_sh = skeletonHelper.SkeletonHelper(name='{}R{}Push{}_{}_{}'.format(descriptor,
                                                                             rotation_axis,
                                                                             suffix,
                                                                             side,
                                                                             usageLib.skin_joint))
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
                                                                          usageLib.clamp))

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
                                                                                      usageLib.multiply))

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
