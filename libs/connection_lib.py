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
        cmds.connectAttr(f'{driver}.{attr}{axis}', f'{driven}.{attr}{axis}', force=True)


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
    return f'{node_desc}{node_usage.capitalize()}_{node_side}_{usage}'


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
    start_usage_capitalize = f'{start_usage[0].upper()}{start_usage[1:]}'

    driver_descriptor, driver_side, driver_usage = driver.split('_')

    start_point_mat_mult = cmds.createNode('pointMatrixMult', name='{}{}_{}_{}'.format(start_descriptor,
                                                                                       start_usage_capitalize,
                                                                                       start_side,
                                                                                       usage_lib.point_matrix_mult))

    cmds.connectAttr(f'{start_joint}.parentMatrix', f'{start_point_mat_mult}.inMatrix')
    cmds.connectAttr(f'{start_joint}.translate', f'{start_point_mat_mult}.inPoint')

    start_point_compose = cmds.createNode('composeMatrix', name='{}{}_{}_{}'.format(start_descriptor,
                                                                                    start_usage_capitalize,
                                                                                    start_side,
                                                                                    usage_lib.compose_matrix))

    cmds.connectAttr(f'{start_point_mat_mult}.output', f'{start_point_compose}.inputTranslate')

    start_point_inverse_matrix = cmds.createNode('inverseMatrix', name='{}{}_{}_{}'.format(start_descriptor,
                                                                                           start_usage_capitalize,
                                                                                           start_side,
                                                                                           usage_lib.inverse_matrix))

    cmds.connectAttr(f'{start_point_compose}.outputMatrix',
                     f'{start_point_inverse_matrix}.inputMatrix')

    pole_vector_mult_mat = cmds.createNode('multMatrix', name='{}_{}_{}'.format(driver_descriptor,
                                                                                driver_side,
                                                                                usage_lib.mult_matrix))

    cmds.connectAttr(f'{driver}.worldMatrix', f'{pole_vector_mult_mat}.matrixIn[0]')

    cmds.connectAttr(f'{start_point_inverse_matrix}.outputMatrix',
                     f'{pole_vector_mult_mat}.matrixIn[1]')

    pole_vector_decompose = cmds.createNode('decomposeMatrix', name='{}_{}_{}'.format(driver_descriptor,
                                                                                      driver_side,
                                                                                      usage_lib.decompose_matrix))

    cmds.connectAttr(f'{pole_vector_mult_mat}.matrixSum',
                     f'{pole_vector_decompose}.inputMatrix')

    cmds.connectAttr(f'{pole_vector_decompose}.outputTranslate',
                     f'{driven}.poleVector')


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
    
    cmds.connectAttr(input_matrix, f'{aim_mat}.inputMatrix')
    
    cmds.connectAttr(primary_target_matrix, f'{aim_mat}.primaryTargetMatrix')
    cmds.setAttr(f'{aim_mat}.primaryInputAxisX', primary_input_axis[0])
    cmds.setAttr(f'{aim_mat}.primaryInputAxisY', primary_input_axis[1])
    cmds.setAttr(f'{aim_mat}.primaryInputAxisZ', primary_input_axis[2])

    if secondary_target_matrix:
        cmds.connectAttr(secondary_target_matrix, f'{aim_mat}.secondaryTargetMatrix')
    cmds.setAttr(f'{aim_mat}.secondaryInputAxisX', secondary_input_axis[0])
    cmds.setAttr(f'{aim_mat}.secondaryInputAxisY', secondary_input_axis[1])
    cmds.setAttr(f'{aim_mat}.secondaryInputAxisZ', secondary_input_axis[2])

    cmds.connectAttr(f'{aim_mat}.outputMatrix', driven, force=True)


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
                              name=f'{descriptor}{usage.capitalize()}_{side}_{usage_lib.mult_matrix}')

    if world:
        driven_matrix = cmds.getAttr(f'{driven}.worldMatrix')
        driver_inverse_matrix = cmds.getAttr(f'{driver}.worldInverseMatrix')
        matrix_difference = math_lib.multiply_matrices_4_by_4(driven_matrix, driver_inverse_matrix)
        cmds.setAttr(f'{mult_matrix}.matrixIn[0]', matrix_difference, type='matrix')
        cmds.connectAttr(f'{driver}.worldMatrix', f'{mult_matrix}.matrixIn[1]')

    else:
        matrix_difference = cmds.getAttr(f'{driven}.worldMatrix')
        cmds.connectAttr(f'{driver}.matrix', f'{mult_matrix}.matrixIn[0]')
        cmds.setAttr(f'{mult_matrix}.matrixIn[1]', matrix_difference, type='matrix')

    if translate and rotate and scale and shear:
        cmds.connectAttr(f'{mult_matrix}.matrixSum', f'{driven}.offsetParentMatrix')
    else:
        pick_mat = cmds.createNode('pickMatrix', name=f'{descriptor}_{side}_{usage_lib.pick_matrix}')
        cmds.connectAttr(f'{mult_matrix}.matrixSum', f'{pick_mat}.inputMatrix')

        if not translate:
            cmds.setAttr(f'{pick_mat}.useTranslate', 0)
        if not rotate:
            cmds.setAttr(f'{pick_mat}.useRotate', 0)
        if not scale:
            cmds.setAttr(f'{pick_mat}.useScale', 0)
        if not shear:
            cmds.setAttr(f'{pick_mat}.useShear', 0)

        cmds.connectAttr(f'{pick_mat}.outputMatrix', f'{driven}.offsetParentMatrix')

    for attr in 'trs':
        value = 0 if attr != 's' else 1
        for axis in 'xyz':
            if cmds.getAttr(f'{driven}.{attr}{axis}', settable=True):
                cmds.setAttr(f'{driven}.{attr}{axis}', value)
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
    attr_capitalize = f'{attr[0].upper()}{attr[1:]}'

    mult_matrix = cmds.createNode('multMatrix', name='{}{}_{}_{}'.format(descriptor,
                                                                         attr_capitalize,
                                                                         side,
                                                                         usage_lib.mult_matrix))
    
    cmds.setAttr(f'{mult_matrix}.matrixIn[0]', cmds.getAttr(f'{driver}.worldInverseMatrix'),
                 type='matrix')
    cmds.connectAttr(f'{driver}.worldMatrix', f'{mult_matrix}.matrixIn[1]')

    if translate and rotate and scale and shear:
        cmds.connectAttr(f'{mult_matrix}.matrixSum', driven_and_attr)
    else:
        pick_mat = cmds.createNode('pickMatrix', name=f'{descriptor}_{side}_{usage_lib.pick_matrix}')
        cmds.connectAttr(f'{mult_matrix}.matrixSum', f'{pick_mat}.inputMatrix')

        if not translate:
            cmds.setAttr(f'{pick_mat}.useTranslate', 0)
        if not rotate:
            cmds.setAttr(f'{pick_mat}.useRotate', 0)
        if not scale:
            cmds.setAttr(f'{pick_mat}.useScale', 0)
        if not shear:
            cmds.setAttr(f'{pick_mat}.useShear', 0)

        cmds.connectAttr(f'{pick_mat}.outputMatrix', driven_and_attr)


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
    mult_matrix = f'{descriptor}{usage.capitalize()}_{side}_{usage_lib.mult_matrix}'

    if not cmds.objExists(mult_matrix):
        mult_matrix = cmds.createNode('multMatrix', name=mult_matrix)

    driver_inverse_matrix = cmds.createNode('inverseMatrix')
    cmds.connectAttr(driver_and_attr, f'{driver_inverse_matrix}.inputMatrix')
    
    matrix_difference = math_lib.multiply_matrices_4_by_4(
        matrix_a=cmds.getAttr(f'{driven}.worldMatrix'),
        matrix_b=cmds.getAttr(f'{driver_inverse_matrix}.outputMatrix'))

    cmds.setAttr(f'{mult_matrix}.matrixIn[0]', matrix_difference, type='matrix')
    cmds.connectAttr(driver_and_attr, f'{mult_matrix}.matrixIn[1]', force=True)

    cmds.delete(driver_inverse_matrix)
    
    if translate and rotate and scale and shear:
        cmds.connectAttr(f'{mult_matrix}.matrixSum', f'{driven}.offsetParentMatrix')
    else:
        pick_mat = cmds.createNode('pickMatrix', 
                                   name='{}{}_{}_{}'.format(descriptor, 
                                                            usage_lib.get_usage_capitalize(usage=usage),
                                                            side, 
                                                            usage_lib.pick_matrix))
        cmds.connectAttr(f'{mult_matrix}.matrixSum', f'{pick_mat}.inputMatrix')

        if not translate:
            cmds.setAttr(f'{pick_mat}.useTranslate', 0)
        if not rotate:
            cmds.setAttr(f'{pick_mat}.useRotate', 0)
        if not scale:
            cmds.setAttr(f'{pick_mat}.useScale', 0)
        if not shear:
            cmds.setAttr(f'{pick_mat}.useShear', 0)

        cmds.connectAttr(f'{pick_mat}.outputMatrix', f'{driven}.offsetParentMatrix')

    for attr in 'trs':
        value = 0 if attr != 's' else 1
        for axis in 'xyz':
            if cmds.getAttr(f'{driven}.{attr}{axis}', settable=True):
                cmds.setAttr(f'{driven}.{attr}{axis}', value)

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

    cmds.setAttr(f'{node}.offsetParentMatrix', node_matrix, type='matrix')

    for attr in ['translate', 'rotate', 'scale']:
        for axis in 'XYZ':
            value = 0 if attr != 'scale' else 1
            if cmds.getAttr(f'{node}.{attr}{axis}', settable=True):
                cmds.setAttr(f'{node}.{attr}{axis}', value)


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

    cmds.setAttr(f'{node}.offsetParentMatrix', math_lib.identity_matrix, type='matrix')

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

    descriptor = f"{crv.split('_')[0]}Crv{cv}"
    side = crv_and_cv.split('_')[1]

    cv_pos = cmds.getAttr(crv_and_cv)[0]
    mult_matrix = cmds.createNode('multMatrix', name=f'{descriptor}_{side}_{usage_lib.mult_matrix}')
    cmds.setAttr(f'{mult_matrix}.matrixIn[0]',
                 math_lib.multiply_matrices_4_by_4(matrix_b=cmds.getAttr(f'{driver}.worldInverseMatrix'),
                                                  matrix_a=[1, 0, 0, 0,
                                                            0, 1, 0, 0,
                                                            0, 0, 1, 0,
                                                            cv_pos[0], cv_pos[1], cv_pos[2], 1]),
                 type='matrix')
    cmds.connectAttr(f'{driver}.worldMatrix', f'{mult_matrix}.matrixIn[1]')

    point_matrix_mult = cmds.createNode('pointMatrixMult', name='{}_{}_{}'.format(descriptor,
                                                                                  side,
                                                                                  usage_lib.point_matrix_mult))

    cmds.connectAttr(f'{mult_matrix}.matrixSum', f'{point_matrix_mult}.inMatrix')

    cmds.connectAttr(f'{point_matrix_mult}.output', f'{crv}.controlPoints[{cv}]')


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

    uvpin_node = cmds.createNode('uvPin', name=f'{descriptor}_{side}_{usage_lib.uvpin}')

    cmds.setAttr(f'{uvpin_node}.normalAxis', 1)
    cmds.setAttr(f'{uvpin_node}.tangentAxis', 0)
    cmds.setAttr(f'{uvpin_node}.normalAxis', 2)

    cmds.connectAttr(f'{nurbs_shape}.worldSpace[0]', f'{uvpin_node}.deformedGeometry')

    # Connections for each driven
    index = 0
    for node in node_list:
        node_descriptor, node_side, node_usage = node.split('_')
        transform_temp = cmds.createNode('transform')
        cmds.xform(transform_temp, worldSpace=True, matrix=cmds.xform(node, query=True, worldSpace=True, matrix=True))
        cpos_temp = cmds.createNode('closestPointOnSurface')

        cmds.connectAttr(f'{nurbs_shape}.worldSpace[0]', f'{cpos_temp}.inputSurface')
        cmds.connectAttr(f'{transform_temp}.translate', f'{cpos_temp}.inPosition')

        u_value = cmds.getAttr(f'{cpos_temp}.parameterU')
        v_value = cmds.getAttr(f'{cpos_temp}.parameterV')

        cmds.setAttr(f'{uvpin_node}.coordinate[{index}].coordinateU', u_value)
        cmds.setAttr(f'{uvpin_node}.coordinate[{index}].coordinateV', v_value)
        
        if maintain_offset:
            connect_matrix_from_attribute(driver_and_attr=f'{uvpin_node}.outputMatrix[{index}]',
                                          driven=node,
                                          translate=translate,
                                          rotate=rotate,
                                          scale=scale,
                                          shear=shear)
        else:
            if translate and rotate and scale and shear:
                cmds.connectAttr(f'{uvpin_node}.outputMatrix[{index}]',
                                 f'{node}.offsetParentMatrix')
            else:
                pick_mat = cmds.createNode('pickMatrix',
                                           name='{}{}_{}_{}'.format(node_descriptor,
                                                                    usage_lib.get_usage_capitalize(usage=node_usage),
                                                                    node_side,
                                                                    usage_lib.pick_matrix))
                cmds.connectAttr(f'{uvpin_node}.outputMatrix[{index}]', f'{pick_mat}.inputMatrix')

                if not translate:
                    cmds.setAttr(f'{pick_mat}.useTranslate', 0)
                if not rotate:
                    cmds.setAttr(f'{pick_mat}.useRotate', 0)
                if not scale:
                    cmds.setAttr(f'{pick_mat}.useScale', 0)
                if not shear:
                    cmds.setAttr(f'{pick_mat}.useShear', 0)

                cmds.connectAttr(f'{pick_mat}.outputMatrix', f'{node}.offsetParentMatrix')


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
            base_output = f'{base}.worldMatrix'
            base_inverse_matrix = cmds.getAttr(f'{base}.worldInverseMatrix')

        base_capitalize_descriptor = '{}{}{}'.format(base_descriptor[0].upper(), base_descriptor[1:], 
                                                     base_usage.capitalize())

    else:
        base_inverse_matrix = cmds.getAttr(f'{driven}.worldInverseMatrix')
        base_capitalize_descriptor = ''

    # base multmat
    if base:
        base_mult_matrix = '{}{}_{}_{}'.format(driven_descriptor,
                                               base_capitalize_descriptor,
                                               driven_side,
                                               usage_lib.mult_matrix)

        if not cmds.objExists(base_mult_matrix):
            base_mult_matrix = cmds.createNode('multMatrix', name=base_mult_matrix)
            cmds.connectAttr(base_output, f'{base_mult_matrix}.matrixIn[1]')

        cmds.setAttr(f'{base_mult_matrix}.matrixIn[0]',
                     math_lib.multiply_matrices_4_by_4(matrix_a=driven_matrix, matrix_b=base_inverse_matrix), type='matrix')

    # driver
    if '.' in driver:
        driver_descriptor = driver.split('.')[-1].split('_')[0]
        driver_capitalize_descriptor = f'{driver_descriptor[0].upper()}{driver_descriptor[1:]}'
        driver_output = driver
        driver_inverse_matrix = math_lib.inverse_matrix(cmds.getAttr(driver))
    else:
        driver_descriptor = driver.split('_')[0]
        driver_capitalize_descriptor = f'{driver_descriptor[0].upper()}{driver_descriptor[1:]}'
        driver_output = f'{driver}.worldMatrix'
        driver_inverse_matrix = cmds.getAttr(f'{driver}.worldInverseMatrix')

    # driver multmat
    driver_mult_matrix = cmds.createNode('multMatrix', name='{}{}_{}_{}'.format(driven_descriptor,
                                                                                driver_capitalize_descriptor,
                                                                                driven_side,
                                                                                usage_lib.mult_matrix))
    cmds.setAttr(f'{driver_mult_matrix}.matrixIn[0]',
                 math_lib.multiply_matrices_4_by_4(matrix_a=driven_matrix,
                                                   matrix_b=driver_inverse_matrix), type='matrix')

    cmds.connectAttr(driver_output, f'{driver_mult_matrix}.matrixIn[1]')

    # blendMatrix
    blend_matrix = '{}{}_{}_{}'.format(driven_descriptor,
                                       driven_usage.capitalize(),
                                       driven_side,
                                       usage_lib.blend_matrix)
    if not cmds.objExists(blend_matrix):
        blend_matrix = cmds.createNode('blendMatrix', name=blend_matrix)
        if base:
            cmds.connectAttr(f'{base_mult_matrix}.matrixSum', f'{blend_matrix}.inputMatrix')
        else:
            cmds.setAttr(f'{blend_matrix}.inputMatrix',
                         cmds.xform(driven, query=True, worldSpace=True, matrix=True),
                         type='matrix')

    target_index_list = cmds.ls(f'{blend_matrix}.target[*]')
    target_index = 0
    if len(target_index_list) != 0:
        target_index = int(max(target_index_list).split('[')[-1].split(']')[0]) + 1

    target_index = f'target[{target_index}]'

    cmds.connectAttr(f'{driver_mult_matrix}.matrixSum', f'{blend_matrix}.{target_index}.targetMatrix')

    # Store old multMatrix
    mult_mat_connection = cmds.listConnections(f'{driven}.offsetParentMatrix')
    if mult_mat_connection:
        mult_mat_connection = [x for x in cmds.listConnections(f'{driven}.offsetParentMatrix')
                               if x.endswith(usage_lib.mult_matrix)]

    # new offsetParentMatrix connection
    if not cmds.isConnected(f'{blend_matrix}.outputMatrix',
                            f'{driven}.offsetParentMatrix'):
        cmds.connectAttr(f'{blend_matrix}.outputMatrix',
                         f'{driven}.offsetParentMatrix', force=True)

    cmds.setAttr(f'{blend_matrix}.{target_index}.translateWeight', 0)
    cmds.setAttr(f'{blend_matrix}.{target_index}.rotateWeight', 0)
    cmds.setAttr(f'{blend_matrix}.{target_index}.scaleWeight', 0)
    cmds.setAttr(f'{blend_matrix}.{target_index}.shearWeight', 0)

    # Add follow attr
    driven_ah = attribute_lib.Helper(driven)
    driven_ah.add_separator_attribute(separator_name='Follows')

    if follow_name:
        follow_name = follow_name
    else:
        follow_name = f'follow{driver_capitalize_descriptor}'

    if pos:
        attr_name = f'{follow_name}Pos'
        driven_ah.add_float_attribute(attr_name, minValue=0, maxValue=1, defaultValue=default_value)
        cmds.connectAttr(f'{driven}.{attr_name}', f'{blend_matrix}.{target_index}.translateWeight')

    if rot:
        attr_name = f'{follow_name}Rot'
        driven_ah.add_float_attribute(attr_name, minValue=0, maxValue=1, defaultValue=default_value)
        cmds.connectAttr(f'{driven}.{attr_name}', f'{blend_matrix}.{target_index}.rotateWeight')

    if not pos and not rot:
        attr_name = follow_name
        driven_ah.add_float_attribute(attr_name, minValue=0, maxValue=1, defaultValue=default_value)
        cmds.connectAttr(f'{driven}.{attr_name}', f'{blend_matrix}.{target_index}.translateWeight')
        cmds.connectAttr(f'{driven}.{attr_name}', f'{blend_matrix}.{target_index}.rotateWeight')

    # Delete stored mult matrix if they do not have connections
    if mult_mat_connection:
         if not cmds.listConnections(mult_mat_connection[0], destination=True, source=False):
             cmds.delete(mult_mat_connection[0])

    return blend_matrix
