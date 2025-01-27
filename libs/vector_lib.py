# Maya imports
from maya import cmds

# Project import
from hiddenStrings.libs import side_lib, usage_lib


def create_pma_vector_from_a_to_b(a, b):
    """
    Create a plus minus average (vector) for a to b in worldSpace

    Args:
        a (str): a node's name
        b (str): b node's name
    
    Returns:
        str: plusMinusAverage node
    """
    if len(a.split('_')) == 3:
        desc_a, side_a, usage_a = a.split('_')
    else:
        desc_a = a
        side_a = side_lib.center
        usage_a = ''
    a_pmatmult = f'{desc_a}{usage_a.capitalize()}_{side_a}_{usage_lib.point_matrix_mult}'
    if not cmds.objExists(a_pmatmult):
        a_pmatmult = cmds.createNode('pointMatrixMult', name=a_pmatmult)
        cmds.connectAttr(f'{a}.worldMatrix', f'{a_pmatmult}.inMatrix')

    if len(b.split('_')) == 3:
        desc_b, side_b, usage_b = b.split('_')
    else:
        desc_b = b
        side_b = side_lib.center
        usage_b = ''
    b_pmatmult = f'{desc_b}{usage_b.capitalize()}_{side_b}_{usage_lib.point_matrix_mult}'
    if not cmds.objExists(b_pmatmult):
        b_pmatmult = cmds.createNode('pointMatrixMult', name=b_pmatmult)
        cmds.connectAttr(f'{b}.worldMatrix', f'{b_pmatmult}.inMatrix')

    pma_node = cmds.createNode('plusMinusAverage', name='{}{}{}Vector_{}_{}'.format(desc_a,
                                                                                    desc_b[0].upper(), desc_b[1:],
                                                                                    side_a,
                                                                                    usage_lib.plus_minus_Average))
    cmds.setAttr(f'{pma_node}.operation', 2)
    cmds.connectAttr(f'{b_pmatmult}.output', f'{pma_node}.input3D[0]')
    cmds.connectAttr(f'{a_pmatmult}.output', f'{pma_node}.input3D[1]')

    return pma_node


def create_angle_between_two_pma_nodes(a, b):
    """
    create an angle between node between two plus minus average

    Args:
        a (str): a node's name
        b (str): b node's name
    
    Returns:
        float: angleBetween.angle value
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
    cmds.connectAttr(f'{a}.output3D', f'{angle_between}.vector1')
    cmds.connectAttr(f'{b}.output3D', f'{angle_between}.vector2')

    return f'{angle_between}.angle'
