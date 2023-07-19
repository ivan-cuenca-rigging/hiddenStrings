# Maya imports
from maya import cmds

# Project import
from hiddenStrings.libs import side_lib, usage_lib


def create_pma_vector_from_a_to_b(a, b):
    """
    Create a plus minus average (vector) for a to b in worldSpace
    :param a: str
    :param b: str
    return plusMinusAverage
    """
    if len(a.split('_')) == 3:
        desc_a, side_a, usage_a = a.split('_')
    else:
        desc_a = a
        side_a = side_lib.center
        usage_a = ''
    a_pmatmult = '{}{}_{}_{}'.format(desc_a, usage_a.capitalize(), side_a, usage_lib.point_matrix_mult)
    if not cmds.objExists(a_pmatmult):
        a_pmatmult = cmds.createNode('pointMatrixMult', name=a_pmatmult)
        cmds.connectAttr('{}.worldMatrix'.format(a), '{}.inMatrix'.format(a_pmatmult))

    if len(b.split('_')) == 3:
        desc_b, side_b, usage_b = b.split('_')
    else:
        desc_b = b
        side_b = side_lib.center
        usage_b = ''
    b_pmatmult = '{}{}_{}_{}'.format(desc_b, usage_b.capitalize(), side_b, usage_lib.point_matrix_mult)
    if not cmds.objExists(b_pmatmult):
        b_pmatmult = cmds.createNode('pointMatrixMult', name=b_pmatmult)
        cmds.connectAttr('{}.worldMatrix'.format(b), '{}.inMatrix'.format(b_pmatmult))

    pma_node = cmds.createNode('plusMinusAverage', name='{}{}{}Vector_{}_{}'.format(desc_a,
                                                                                    desc_b[0].upper(), desc_b[1:],
                                                                                    side_a,
                                                                                    usage_lib.plus_minus_Average))
    cmds.setAttr('{}.operation'.format(pma_node), 2)
    cmds.connectAttr('{}.output'.format(b_pmatmult), '{}.input3D[0]'.format(pma_node))
    cmds.connectAttr('{}.output'.format(a_pmatmult), '{}.input3D[1]'.format(pma_node))

    return pma_node


def create_angle_between_two_pma_nodes(a, b):
    """
    create an angle between node between two plus minus average
    :param a: str
    :param b: str
    return angle between angle attribute
    """
    if len(a.split('_')) == 3:
        desc_a, side_a, usage_a = a.split('_')
    else:
        desc_a = a
        side_a = side_lib.center

    if len(b.split('_')) == 3:
        desc_b, side_b, usage_b = b.split('_')
    else:
        desc_b = b

    angle_between = cmds.createNode('angleBetween', name='{}{}{}_{}_{}'.format(desc_a,
                                                                               desc_b[0], desc_b[1:],
                                                                               side_a,
                                                                               usage_lib.angle_between))
    cmds.connectAttr('{}.output3D'.format(a), '{}.vector1'.format(angle_between))
    cmds.connectAttr('{}.output3D'.format(b), '{}.vector2'.format(angle_between))

    return '{}.angle'.format(angle_between)
