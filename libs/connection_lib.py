# Imports
import logging

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import side_lib, usage_lib, math_lib, attribute_lib

logging = logging.getLogger(__name__)


def connect_3_axis(driver, driven, attr):
    """
    Connect the 3 axis

    Args:
        driver (str): name of the driver
        driven (str): name of the driven
        attr (str): name of the attribute
    """
    for axis in ['X', 'Y', 'Z']:
        cmds.connectAttr('{}.{}{}'.format(driver, attr, axis), '{}.{}{}'.format(driven, attr, axis), force=True)


def connect_translate(driver, driven):
    """
    Connect the translation

    Args:
        driver (str): name of the driver
        driven (str): name of the driven
    """
    connect_3_axis(driver, driven, 'translate')


def connect_rotate(driver, driven):
    """
    Connect the rotation

    Args:
        driver (str): name of the driver
        driven (str): name of the driven
    """
    connect_3_axis(driver, driven, 'rotate')


def connect_scale(driver, driven):
    """
    Connect the scale

    Args:
        driver (str): name of the driver
        driven (str): name of the driven
    """
    connect_3_axis(driver, driven, 'scale')


def connect_translate_rotate_scale(driver, driven):
    """
    Connect the translation, translation and scale

    Args:
        driver (str): name of the driver
        driven (str): name of the driven
    """
    connect_translate(driver, driven)
    connect_rotate(driver, driven)
    connect_scale(driver, driven)


def format_constraint_name(driven, usage):
    """
    Format the name of the constraint

    Args:
        driven (str): name of the driven
        usage (str): usage of the constraint

    Returns:
        str: constraint name format
    """
    node_desc, node_side, node_usage = driven.split('_')
    return '{}{}_{}_{}'.format(node_desc, node_usage.capitalize(), node_side, usage)


def create_parent_constraint(driver, driven, *args, **kwargs):
    """
    Create a parentConstraint

    Args:
        driver (str): name of the driver
        driven (str): name of the driven

    Returns:
        str: parentConstraint name
    """
    return cmds.parentConstraint(driver,
                                 driven,
                                 name=format_constraint_name(driven, usage_lib.parent_constraint),
                                 *args, **kwargs)


def create_orient_constraint(driver, driven, *args, **kwargs):
    """
    Create a orientConstraint

    Args:
        driver (str): name of the driver
        driven (str): name of the driven

    Returns:
        str: orientConstraint name
    """
    cns = cmds.orientConstraint(driver,
                                driven,
                                name=format_constraint_name(driven, usage_lib.orient_constraint),
                                *args, **kwargs)
    return cns[0]


def create_point_constraint(driver, driven, *args, **kwargs):
    """
    Create a pointConstraint

    Args:
        driver (str): name of the driver
        driven (str): name of the driven

    Returns:
        str: pointConstraint name
    """
    cns = cmds.pointConstraint(driver,
                               driven,
                               name=format_constraint_name(driven, usage_lib.point_constraint),
                               *args, **kwargs)
    return cns[0]


def create_scale_constraint(driver, driven, *args, **kwargs):
    """
    Create a scaleConstraint

    Args:
        driver (str): name of the driver
        driven (str): name of the driven

    Returns:
        str: scaleConstraint name
    """
    cns = cmds.scaleConstraint(driver,
                               driven,
                               name=format_constraint_name(driven, usage_lib.scale_constraint),
                               *args, **kwargs)
    return cns[0]


def create_aim_constraint(driver, driven, *args, **kwargs):
    """
    Create a aimConstraint

    Args:
        driver (str): name of the driver
        driven (str): name of the driven

    Returns:
        str: aimConstraint name
    """
    cns = cmds.aimConstraint(driver,
                             driven,
                             name=format_constraint_name(driven, usage_lib.aim_constraint),
                             *args, **kwargs)
    return cns[0]


def create_pole_constraint(driver, driven, *args, **kwargs):
    """
    Create a poleVectorConstraint

    Args:
        driver (str): name of the driver
        driven (str): name of the driven

    Returns:
        str: poleVectorConstraint name
    """
    cns = cmds.poleVectorConstraint(driver,
                                    driven,
                                    name=format_constraint_name(driven, usage_lib.pole_vector_constraint),
                                    *args, **kwargs)
    return cns[0]


def create_pole_with_matrices(driver, driven, start_joint):
    """
    Create a pole vector constraint but with matrix nodes

    Args:
        driver (str): name of the driver
        driven (str): name of the driven
        start_joint (str): name of the start joint
    """
    start_descriptor, start_side, start_usage = start_joint.split('_')
    start_usage_capitalize = '{}{}'.format(start_usage[0].upper(), start_usage[1:])

    driver_descriptor, driver_side, driver_usage = driver.split('_')

    start_point_mat_mult = cmds.createNode('pointMatrixMult', name='{}{}_{}_{}'.format(start_descriptor,
                                                                                       start_usage_capitalize,
                                                                                       start_side,
                                                                                       usage_lib.point_matrix_mult))

    cmds.connectAttr('{}.parentMatrix'.format(start_joint), '{}.inMatrix'.format(start_point_mat_mult))
    cmds.connectAttr('{}.translate'.format(start_joint), '{}.inPoint'.format(start_point_mat_mult))

    start_point_compose = cmds.createNode('composeMatrix', name='{}{}_{}_{}'.format(start_descriptor,
                                                                                    start_usage_capitalize,
                                                                                    start_side,
                                                                                    usage_lib.compose_matrix))

    cmds.connectAttr('{}.output'.format(start_point_mat_mult), '{}.inputTranslate'.format(start_point_compose))

    start_point_inverse_matrix = cmds.createNode('inverseMatrix', name='{}{}_{}_{}'.format(start_descriptor,
                                                                                           start_usage_capitalize,
                                                                                           start_side,
                                                                                           usage_lib.inverse_matrix))

    cmds.connectAttr('{}.outputMatrix'.format(start_point_compose),
                     '{}.inputMatrix'.format(start_point_inverse_matrix))

    pole_vector_mult_mat = cmds.createNode('multMatrix', name='{}_{}_{}'.format(driver_descriptor,
                                                                                driver_side,
                                                                                usage_lib.mult_matrix))

    cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.matrixIn[0]'.format(pole_vector_mult_mat))

    cmds.connectAttr('{}.outputMatrix'.format(start_point_inverse_matrix),
                     '{}.matrixIn[1]'.format(pole_vector_mult_mat))

    pole_vector_decompose = cmds.createNode('decomposeMatrix', name='{}_{}_{}'.format(driver_descriptor,
                                                                                      driver_side,
                                                                                      usage_lib.decompose_matrix))

    cmds.connectAttr('{}.matrixSum'.format(pole_vector_mult_mat),
                     '{}.inputMatrix'.format(pole_vector_decompose))

    cmds.connectAttr('{}.outputTranslate'.format(pole_vector_decompose),
                     '{}.poleVector'.format(driven))


def create_aim_matrix(input_matrix, 
                      primary_target_matrix,
                      driven,
                      secondary_target_matrix=None,
                      primary_input_axis=[0, 0, 1],
                      secondary_input_axis=[0, 1, 0]):
    """
    Create aim matrix

    Args:
        input_matrix (str): node.attribute
        primary_target_matrix (str): node.attribute
        driven (str): node
        secondary_target_matrix (str, optional): node.attribute. Defaults to None.
        primary_input_axis (list, optional): aim vector. Defaults to (0, 0, 1).
        secondary_input_axis (list, optional): up vector. Defaults to (0, 1, 0).
    """
    desc, side, usage = driven.split('.')[0].split('_')
    aim_mat = cmds.createNode('aimMatrix', name='{}{}_{}_{}'.format(desc, usage.capitalize(), 
                                                                    side, usage_lib.aim_matrix))
    
    cmds.connectAttr(input_matrix, '{}.inputMatrix'.format(aim_mat))
    
    cmds.connectAttr(primary_target_matrix, '{}.primaryTargetMatrix'.format(aim_mat))
    cmds.setAttr('{}.primaryInputAxisX'.format(aim_mat), primary_input_axis[0])
    cmds.setAttr('{}.primaryInputAxisY'.format(aim_mat), primary_input_axis[1])
    cmds.setAttr('{}.primaryInputAxisZ'.format(aim_mat), primary_input_axis[2])

    if secondary_target_matrix:
        cmds.connectAttr(secondary_target_matrix, '{}.secondaryTargetMatrix'.format(aim_mat))
    cmds.setAttr('{}.secondaryInputAxisX'.format(aim_mat), secondary_input_axis[0])
    cmds.setAttr('{}.secondaryInputAxisY'.format(aim_mat), secondary_input_axis[1])
    cmds.setAttr('{}.secondaryInputAxisZ'.format(aim_mat), secondary_input_axis[2])

    cmds.connectAttr('{}.outputMatrix'.format(aim_mat), driven, force=True)


def connect_offset_parent_matrix(driver, driven,
                                 translate=True,
                                 rotate=True,
                                 scale=True,
                                 shear=True,
                                 world=True):
    """
    Connect driver to the offsetParentMatrix of the driven

    Args:
        driver (str): name of the driver
        driven (str): name of the driven
        translate (bool, optional): connect translate. Defaults to True.
        rotate (bool, optional): connect rotate. Defaults to True.
        scale (bool, optional): connect scale. Defaults to True.
        shear (bool, optional): connect shear. Defaults to True.
        world (bool, optional): True == worldMatrix. Defaults to True.

    Returns:
        str: multMatrix node name
    """
    if len(driven.split('_')) != 3:
        descriptor = driven
        side = side_lib.center
        usage = ''
        logging.info('Names should have 3 fields {descriptor}_{side}_{usage}.')
    else:
        descriptor, side, usage = driven.split('_')

    # Logic
    mult_matrix = cmds.createNode('multMatrix',
                              name='{}{}_{}_{}'.format(descriptor, usage.capitalize(), side, usage_lib.mult_matrix))

    if world:
        driven_matrix = cmds.getAttr('{}.worldMatrix'.format(driven))
        driver_inverse_matrix = cmds.getAttr('{}.worldInverseMatrix'.format(driver))
        matrix_difference = math_lib.multiply_matrices_4_by_4(driven_matrix, driver_inverse_matrix)
        cmds.setAttr('{}.matrixIn[0]'.format(mult_matrix), matrix_difference, type='matrix')
        cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.matrixIn[1]'.format(mult_matrix))

    else:
        matrix_difference = cmds.getAttr('{}.worldMatrix'.format(driven))
        cmds.connectAttr('{}.matrix'.format(driver), '{}.matrixIn[0]'.format(mult_matrix))
        cmds.setAttr('{}.matrixIn[1]'.format(mult_matrix), matrix_difference, type='matrix')

    if translate and rotate and scale and shear:
        cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.offsetParentMatrix'.format(driven))
    else:
        pick_mat = cmds.createNode('pickMatrix', name='{}_{}_{}'.format(descriptor, side, usage_lib.pick_matrix))
        cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.inputMatrix'.format(pick_mat))

        if not translate:
            cmds.setAttr('{}.useTranslate'.format(pick_mat), 0)
        if not rotate:
            cmds.setAttr('{}.useRotate'.format(pick_mat), 0)
        if not scale:
            cmds.setAttr('{}.useScale'.format(pick_mat), 0)
        if not shear:
            cmds.setAttr('{}.useShear'.format(pick_mat), 0)

        cmds.connectAttr('{}.outputMatrix'.format(pick_mat), '{}.offsetParentMatrix'.format(driven))

    for attr in 'trs':
        value = 0 if attr != 's' else 1
        for axis in 'xyz':
            if cmds.getAttr('{}.{}{}'.format(driven, attr, axis), settable=True):
                cmds.setAttr('{}.{}{}'.format(driven, attr, axis), value)
    return mult_matrix


def connect_matrix_to_attribute(driver, driven_and_attr,
                                translate=True,
                                rotate=True,
                                scale=True,
                                shear=True):
    """    
    Connect driver worldMatrix to an attribute, the result matrix will be the identity matrix

    Args:
        driver (str): name of the driver
        driven_and_attr (str): E.G. 'root_c_outputs.root_c_ctr'
        translate (bool, optional): connect translate. Defaults to True.
        rotate (bool, optional): connect rotate. Defaults to True.
        scale (bool, optional): connect scale. Defaults to True.
        shear (bool, optional): connect shear. Defaults to True.
    """
    node, attr = driven_and_attr.split('.')
    descriptor, side, usage = node.split('_')
    if '_' in attr:
        side = attr.split('_')[1]
        attr = attr.split('_')[0] + attr.split('_')[1].capitalize() + attr.split('_')[2].capitalize()
    attr_capitalize = '{}{}'.format(attr[0].upper(), attr[1:])

    mult_matrix = cmds.createNode('multMatrix', name='{}{}_{}_{}'.format(descriptor,
                                                                         attr_capitalize,
                                                                         side,
                                                                         usage_lib.mult_matrix))
    
    cmds.setAttr('{}.matrixIn[0]'.format(mult_matrix), cmds.getAttr('{}.worldInverseMatrix'.format(driver)),
                 type='matrix')
    cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.matrixIn[1]'.format(mult_matrix))

    if translate and rotate and scale and shear:
        cmds.connectAttr('{}.matrixSum'.format(mult_matrix), driven_and_attr)
    else:
        pick_mat = cmds.createNode('pickMatrix', name='{}_{}_{}'.format(descriptor, side, usage_lib.pick_matrix))
        cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.inputMatrix'.format(pick_mat))

        if not translate:
            cmds.setAttr('{}.useTranslate'.format(pick_mat), 0)
        if not rotate:
            cmds.setAttr('{}.useRotate'.format(pick_mat), 0)
        if not scale:
            cmds.setAttr('{}.useScale'.format(pick_mat), 0)
        if not shear:
            cmds.setAttr('{}.useShear'.format(pick_mat), 0)

        cmds.connectAttr('{}.outputMatrix'.format(pick_mat), driven_and_attr)


def connect_matrix_from_attribute(driver_and_attr, driven,
                                  translate=True,
                                  rotate=True,
                                  scale=True,
                                  shear=True):
    """
    Connect an attribute to the offsetParentMatrix of the driven

    Args:
        driver_and_attr (str): E.G. 'root_c_outputs.root_c_ctr'
        driven (str): name of the driven
        translate (bool, optional): connect translate. Defaults to True.
        rotate (bool, optional): connect rotate. Defaults to True.
        scale (bool, optional): connect scale. Defaults to True.
        shear (bool, optional): connect shear. Defaults to True.

    Returns:
        str: mult_matrix
    """
    descriptor, side, usage = driven.split('_')
    mult_matrix = '{}{}_{}_{}'.format(descriptor, usage.capitalize(), side, usage_lib.mult_matrix)

    if not cmds.objExists(mult_matrix):
        mult_matrix = cmds.createNode('multMatrix', name=mult_matrix)

    driver_inverse_matrix = cmds.createNode('inverseMatrix')
    cmds.connectAttr(driver_and_attr, '{}.inputMatrix'.format(driver_inverse_matrix))
    
    matrix_difference = math_lib.multiply_matrices_4_by_4(
        matrix_a=cmds.getAttr('{}.worldMatrix'.format(driven)),
        matrix_b=cmds.getAttr('{}.outputMatrix'.format(driver_inverse_matrix)))

    cmds.setAttr('{}.matrixIn[0]'.format(mult_matrix), matrix_difference, type='matrix')
    cmds.connectAttr(driver_and_attr, '{}.matrixIn[1]'.format(mult_matrix), force=True)

    cmds.delete(driver_inverse_matrix)
    
    if translate and rotate and scale and shear:
        cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.offsetParentMatrix'.format(driven))
    else:
        pick_mat = cmds.createNode('pickMatrix', 
                                   name='{}{}_{}_{}'.format(descriptor, 
                                                            usage_lib.get_usage_capitalize(usage=usage),
                                                            side, 
                                                            usage_lib.pick_matrix))
        cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.inputMatrix'.format(pick_mat))

        if not translate:
            cmds.setAttr('{}.useTranslate'.format(pick_mat), 0)
        if not rotate:
            cmds.setAttr('{}.useRotate'.format(pick_mat), 0)
        if not scale:
            cmds.setAttr('{}.useScale'.format(pick_mat), 0)
        if not shear:
            cmds.setAttr('{}.useShear'.format(pick_mat), 0)

        cmds.connectAttr('{}.outputMatrix'.format(pick_mat), '{}.offsetParentMatrix'.format(driven))

    for attr in 'trs':
        value = 0 if attr != 's' else 1
        for axis in 'xyz':
            if cmds.getAttr('{}.{}{}'.format(driven, attr, axis), settable=True):
                cmds.setAttr('{}.{}{}'.format(driven, attr, axis), value)

    return mult_matrix


def transform_to_offset_parent_matrix(node, world_space=False, *args):
    """
    Set matrix in the offsetParentMatrix and set transform to default

    Args:
        node (str): name of the node
        world_space (bool, optional): True == worldSpace. Defaults to False.
    """
    if not node:
        node = cmds.ls(selection=True)[0]

    if world_space:
        node_matrix = cmds.xform(node, query=True, worldSpace=True, matrix=True)
    else:
        node_matrix = cmds.xform(node, query=True, objectSpace=True, matrix=True)

    cmds.setAttr('{}.offsetParentMatrix'.format(node), node_matrix, type='matrix')

    for attr in ['translate', 'rotate', 'scale']:
        for axis in 'XYZ':
            value = 0 if attr != 'scale' else 1
            if cmds.getAttr('{}.{}{}'.format(node, attr, axis), settable=True):
                cmds.setAttr('{}.{}{}'.format(node, attr, axis), value)


def offset_parent_matrix_to_transform(node, world_space=True, *args):
    """
    Set matrix in the transform and set offsetParentMatrix to default

    Args:
        node (str): name of the node
        world_space (bool, optional): True == worldSpace. Defaults to True.
    """
    if not node:
        node = cmds.ls(selection=True)[0]

    if world_space:
        node_matrix = cmds.xform(node, query=True, worldSpace=True, matrix=True)
    else:
        node_matrix = cmds.xform(node, query=True, objectSpace=True, matrix=True)

    cmds.setAttr('{}.offsetParentMatrix'.format(node), math_lib.identity_matrix, type='matrix')

    if world_space:
        cmds.xform(node, worldSpace=True, matrix=node_matrix)
    else:
        cmds.xform(node, objectSpace=True, matrix=node_matrix)


def connect_point_matrix_mult_to_a_cv(driver, crv_and_cv):
    """
    connect only the position from a worldMatrix to a cv
    
    Args:
        driver (str): name of the driver
        crv_and_cv (str): E.G. 'upArm_l_crvShape.cv[0]'
    """

    crv = crv_and_cv.split('.')[0]
    cv = crv_and_cv.split('[')[-1].split(']')[0]

    descriptor = '{}Crv{}'.format(crv.split('_')[0], cv)
    side = crv_and_cv.split('_')[1]

    cv_pos = cmds.getAttr(crv_and_cv)[0]
    mult_matrix = cmds.createNode('multMatrix', name='{}_{}_{}'.format(descriptor, side, usage_lib.mult_matrix))
    cmds.setAttr('{}.matrixIn[0]'.format(mult_matrix),
                 math_lib.multiply_matrices_4_by_4(matrix_b=cmds.getAttr('{}.worldInverseMatrix'.format(driver)),
                                                  matrix_a=[1, 0, 0, 0,
                                                            0, 1, 0, 0,
                                                            0, 0, 1, 0,
                                                            cv_pos[0], cv_pos[1], cv_pos[2], 1]),
                 type='matrix')
    cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.matrixIn[1]'.format(mult_matrix))

    point_matrix_mult = cmds.createNode('pointMatrixMult', name='{}_{}_{}'.format(descriptor,
                                                                                  side,
                                                                                  usage_lib.point_matrix_mult))

    cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.inMatrix'.format(point_matrix_mult))

    cmds.connectAttr('{}.output'.format(point_matrix_mult), '{}.controlPoints[{}]'.format(crv, cv))


def create_nurbs_uvpin(nurbs, 
                 node_list,
                 maintain_offset=True,
                 translate=True,
                 rotate=True,
                 scale=True,
                 shear=True):
    """
    Create an uvPin

    Args:
        nurbs (str): name of the nurbs
        node_list (list): list of nodes we want to attach to the uvPin
        maintain_offset (bool, optional): maintain offset. Defaults to True.
        translate (bool, optional): connect translate. Defaults to True.
        rotate (bool, optional): connect rotate. Defaults to True.
        scale (bool, optional): connect scale. Defaults to True.
        shear (bool, optional): connect shear. Defaults to True.
    """
    # Checks
    if len(nurbs.split('_')) != 3:
        logging.error('check nurbs name, it should be: {descriptor}_{side}_{usage}')
        raise RuntimeError('Check scriptEditor for further details')
    for node in node_list:
        if len(node.split('_')) != 3:
            print(node.split('_'))
            logging.error('check nodes names, they should be: {descriptor}_{side}_{usage}')
            raise RuntimeError('Check scriptEditor for further details')
    
    #Create uvPin node and connect nurbs
    descriptor, side = nurbs.split('_')[:2]
    nurbs_shape = cmds.listRelatives(nurbs, shapes=True)[0]

    uvpin_node = cmds.createNode('uvPin', name='{}_{}_{}'.format(descriptor, side, usage_lib.uvpin))

    cmds.setAttr('{}.normalAxis'.format(uvpin_node), 1)
    cmds.setAttr('{}.tangentAxis'.format(uvpin_node), 0)
    cmds.setAttr('{}.normalAxis'.format(uvpin_node), 2)

    cmds.connectAttr('{}.worldSpace[0]'.format(nurbs_shape), '{}.deformedGeometry'.format(uvpin_node))

    # Connections for each driven
    index = 0
    for node in node_list:
        node_descriptor, node_side, node_usage = node.split('_')
        transform_temp = cmds.createNode('transform')
        cmds.xform(transform_temp, worldSpace=True, matrix=cmds.xform(node, query=True, worldSpace=True, matrix=True))
        cpos_temp = cmds.createNode('closestPointOnSurface')

        cmds.connectAttr('{}.worldSpace[0]'.format(nurbs_shape), '{}.inputSurface'.format(cpos_temp))
        cmds.connectAttr('{}.translate'.format(transform_temp), '{}.inPosition'.format(cpos_temp))

        u_value = cmds.getAttr('{}.parameterU'.format(cpos_temp))
        v_value = cmds.getAttr('{}.parameterV'.format(cpos_temp))

        cmds.setAttr('{}.coordinate[{}].coordinateU'.format(uvpin_node, index), u_value)
        cmds.setAttr('{}.coordinate[{}].coordinateV'.format(uvpin_node, index), v_value)
        
        if maintain_offset:
            connect_matrix_from_attribute(driver_and_attr='{}.outputMatrix[{}]'.format(uvpin_node, index),
                                        driven=node,
                                        translate=translate,
                                        rotate=rotate,
                                        scale=scale,
                                        shear=shear)
        else:
            if translate and rotate and scale and shear:
                cmds.connectAttr('{}.outputMatrix[{}]'.format(uvpin_node, index),
                                 '{}.offsetParentMatrix'.format(node))
            else:
                pick_mat = cmds.createNode('pickMatrix',
                                           name='{}{}_{}_{}'.format(node_descriptor,
                                                                    usage_lib.get_usage_capitalize(usage=node_usage),
                                                                    node_side,
                                                                    usage_lib.pick_matrix))
                cmds.connectAttr('{}.outputMatrix[{}]'.format(uvpin_node, index), '{}.inputMatrix'.format(pick_mat))

                if not translate:
                    cmds.setAttr('{}.useTranslate'.format(pick_mat), 0)
                if not rotate:
                    cmds.setAttr('{}.useRotate'.format(pick_mat), 0)
                if not scale:
                    cmds.setAttr('{}.useScale'.format(pick_mat), 0)
                if not shear:
                    cmds.setAttr('{}.useShear'.format(pick_mat), 0)

                cmds.connectAttr('{}.outputMatrix'.format(pick_mat), '{}.offsetParentMatrix'.format(node))


        cmds.delete(transform_temp, cpos_temp)
        index += 1


def create_follow(driver,
                  driven,
                  base=None,
                  follow_name=None,
                  rot=False,
                  pos=False,
                  default_value=True):
    """
    Create a follow, if rot or pos is True, the follow will be split

    Args:
        driver (_type_): name of the driver. It can be 'node' or 'node.attribute'
        driven (_type_): name of the driven. It can be 'node' or 'node.attribute'
        base (_type_): name of the base. It can be 'node' or 'node.attribute'. Defaults to None
        follow_name (_type_, optional): name of the follow. Defaults to None.
        rot (bool, optional): follow only rotation. Defaults to False.
        pos (bool, optional): follow only position. Defaults to False.
        default_value (bool, optional): follow value by default. Defaults to True.

    Returns:
        str: blendMatrix output
    """
    # Driven
    driven_descriptor, driven_side, driven_usage = driven.split('_')

    driven_matrix = cmds.xform(driven, query=True, worldSpace=True, matrix=True)

    # Base
    if base:
        if '.' in base:
            base_descriptor = base.split('.')[0].split('_')[0]
            base_usage = base.split('.')[0].split('_')[-1]
            base_output = base
            base_inverse_matrix = math_lib.inverse_matrix(cmds.getAttr(base))
        else:
            base_descriptor = base.split('_')[0]
            base_usage = base.split('_')[-1]
            base_output = '{}.worldMatrix'.format(base)
            base_inverse_matrix = cmds.getAttr('{}.worldInverseMatrix'.format(base))

        base_capitalize_descriptor = '{}{}{}'.format(base_descriptor[0].upper(), base_descriptor[1:], 
                                                     base_usage.capitalize())

    else:
        base_inverse_matrix = cmds.getAttr('{}.worldInverseMatrix'.format(driven))
        base_capitalize_descriptor = ''

    # base multmat
    if base:
        base_mult_matrix = '{}{}_{}_{}'.format(driven_descriptor,
                                               base_capitalize_descriptor,
                                               driven_side,
                                               usage_lib.mult_matrix)

        if not cmds.objExists(base_mult_matrix):
            base_mult_matrix = cmds.createNode('multMatrix', name=base_mult_matrix)
            cmds.connectAttr(base_output, '{}.matrixIn[1]'.format(base_mult_matrix))

        cmds.setAttr('{}.matrixIn[0]'.format(base_mult_matrix),
                     math_lib.multiply_matrices_4_by_4(matrix_a=driven_matrix, matrix_b=base_inverse_matrix), type='matrix')

    # driver
    if '.' in driver:
        driver_descriptor = driver.split('.')[-1].split('_')[0]
        driver_capitalize_descriptor = '{}{}'.format(driver_descriptor[0].upper(), driver_descriptor[1:])
        driver_output = driver
        driver_inverse_matrix = math_lib.inverse_matrix(cmds.getAttr(driver))
    else:
        driver_descriptor = driver.split('_')[0]
        driver_capitalize_descriptor = '{}{}'.format(driver_descriptor[0].upper(), driver_descriptor[1:])
        driver_output = '{}.worldMatrix'.format(driver)
        driver_inverse_matrix = cmds.getAttr('{}.worldInverseMatrix'.format(driver))

    # driver multmat
    driver_mult_matrix = cmds.createNode('multMatrix', name='{}{}_{}_{}'.format(driven_descriptor,
                                                                                driver_capitalize_descriptor,
                                                                                driven_side,
                                                                                usage_lib.mult_matrix))
    cmds.setAttr('{}.matrixIn[0]'.format(driver_mult_matrix),
                 math_lib.multiply_matrices_4_by_4(matrix_a=driven_matrix,
                                                   matrix_b=driver_inverse_matrix), type='matrix')

    cmds.connectAttr(driver_output, '{}.matrixIn[1]'.format(driver_mult_matrix))

    # blendMatrix
    blend_matrix = '{}{}_{}_{}'.format(driven_descriptor,
                                       driven_usage.capitalize(),
                                       driven_side,
                                       usage_lib.blend_matrix)
    if not cmds.objExists(blend_matrix):
        blend_matrix = cmds.createNode('blendMatrix', name=blend_matrix)
        if base:
            cmds.connectAttr('{}.matrixSum'.format(base_mult_matrix), '{}.inputMatrix'.format(blend_matrix))
        else:
            cmds.setAttr('{}.inputMatrix'.format(blend_matrix),
                         cmds.xform(driven, query=True, worldSpace=True, matrix=True),
                         type='matrix')

    target_index_list = cmds.ls('{}.target[*]'.format(blend_matrix))
    target_index = 0
    if len(target_index_list) != 0:
        target_index = int(max(target_index_list).split('[')[-1].split(']')[0]) + 1

    target_index = 'target[{}]'.format(target_index)

    cmds.connectAttr('{}.matrixSum'.format(driver_mult_matrix), '{}.{}.targetMatrix'.format(blend_matrix, target_index))

    # Store old multMatrix
    mult_mat_connection = cmds.listConnections('{}.offsetParentMatrix'.format(driven))
    if mult_mat_connection:
        mult_mat_connection = [x for x in cmds.listConnections('{}.offsetParentMatrix'.format(driven))
                               if x.endswith(usage_lib.mult_matrix)]

    # new offsetParentMatrix connection
    if not cmds.isConnected('{}.outputMatrix'.format(blend_matrix),
                            '{}.offsetParentMatrix'.format(driven)):
        cmds.connectAttr('{}.outputMatrix'.format(blend_matrix),
                         '{}.offsetParentMatrix'.format(driven), force=True)

    cmds.setAttr('{}.{}.translateWeight'.format(blend_matrix, target_index), 0)
    cmds.setAttr('{}.{}.rotateWeight'.format(blend_matrix, target_index), 0)
    cmds.setAttr('{}.{}.scaleWeight'.format(blend_matrix, target_index), 0)
    cmds.setAttr('{}.{}.shearWeight'.format(blend_matrix, target_index), 0)

    # Add follow attr
    driven_ah = attribute_lib.Helper(driven)
    driven_ah.add_separator_attribute(separator_name='Follows')

    if follow_name:
        follow_name = follow_name
    else:
        follow_name = 'follow{}'.format(driver_capitalize_descriptor)

    if pos:
        attr_name = '{}Pos'.format(follow_name)
        driven_ah.add_float_attribute(attr_name, minValue=0, maxValue=1, defaultValue=default_value)
        cmds.connectAttr('{}.{}'.format(driven, attr_name), '{}.{}.translateWeight'.format(blend_matrix, target_index))

    if rot:
        attr_name = '{}Rot'.format(follow_name)
        driven_ah.add_float_attribute(attr_name, minValue=0, maxValue=1, defaultValue=default_value)
        cmds.connectAttr('{}.{}'.format(driven, attr_name), '{}.{}.rotateWeight'.format(blend_matrix, target_index))

    if not pos and not rot:
        attr_name = follow_name
        driven_ah.add_float_attribute(attr_name, minValue=0, maxValue=1, defaultValue=default_value)
        cmds.connectAttr('{}.{}'.format(driven, attr_name), '{}.{}.translateWeight'.format(blend_matrix, target_index))
        cmds.connectAttr('{}.{}'.format(driven, attr_name), '{}.{}.rotateWeight'.format(blend_matrix, target_index))

    # Delete stored mult matrix if they do not have connections
    if mult_mat_connection:
         if not cmds.listConnections(mult_mat_connection[0], destination=True, source=False):
             cmds.delete(mult_mat_connection[0])

    return blend_matrix
