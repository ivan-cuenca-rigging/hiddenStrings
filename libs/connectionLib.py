# Imports
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import sideLib, usageLib, mathLib, jsonLib
from hiddenStrings.libs.helpers import attributeHelper


def connect_3_axis(driver, driven, attr):
    """
    connect attribute's x,y and z
    :param driver: str
    :param driven: str
    :param attr: str
    """
    for axis in ['X', 'Y', 'Z']:
        cmds.connectAttr('{}.{}{}'.format(driver, attr, axis), '{}.{}{}'.format(driven, attr, axis), force=True)


def connect_translate(driver, driven):
    """
    Connect translate
    :param driver: str
    :param driven: str
    """
    connect_3_axis(driver, driven, 'translate')


def connect_rotate(driver, driven):
    """
    Connect rotation
    :param driver: str
    :param driven: str
    """
    connect_3_axis(driver, driven, 'rotate')


def connect_scale(driver, driven):
    """
    Connect scale
    :param driver: str
    :param driven: str
    """
    connect_3_axis(driver, driven, 'scale')


def connect_translate_rotate_scale(driver, driven):
    """
    Connect translate, rotate and scale
    :param driver: str
    :param driven: str
    """
    connect_translate(driver, driven)
    connect_rotate(driver, driven)
    connect_scale(driver, driven)


def format_constraint_name(driven, usage):
    """
    Get constraint's name
    :param driven: str
    :param usage: str
    :return: constraint's name
    """
    node_desc, node_side, node_usage = driven.split('_')
    return '{}{}_{}_{}'.format(node_desc, node_usage.capitalize(), node_side, usage)


def create_parent_constraint(driver, driven, *args, **kwargs):
    """
    Create a parent constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: parent constraint
    """
    return cmds.parentConstraint(driver,
                                 driven,
                                 name=format_constraint_name(driven, usageLib.parent_constraint),
                                 *args, **kwargs)


def create_orient_constraint(driver, driven, *args, **kwargs):
    """
    Create a orient constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: orient constraint
    """
    cns = cmds.orientConstraint(driver,
                                driven,
                                name=format_constraint_name(driven, usageLib.orient_constraint),
                                *args, **kwargs)
    return cns[0]


def create_point_constraint(driver, driven, *args, **kwargs):
    """
    Create a point constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: point constraint
    """
    cns = cmds.pointConstraint(driver,
                               driven,
                               name=format_constraint_name(driven, usageLib.point_constraint),
                               *args, **kwargs)
    return cns[0]


def create_scale_constraint(driver, driven, *args, **kwargs):
    """
    Create a scale constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: scale constraint
    """
    cns = cmds.scaleConstraint(driver,
                               driven,
                               name=format_constraint_name(driven, usageLib.scale_constraint),
                               *args, **kwargs)
    return cns[0]


def create_aim_constraint(driver, driven, *args, **kwargs):
    """
    Create a aim constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: aim constraint
    """
    cns = cmds.aimConstraint(driver,
                             driven,
                             name=format_constraint_name(driven, usageLib.aim_constraint),
                             *args, **kwargs)
    return cns[0]


def create_pole_constraint(driver, driven, *args, **kwargs):
    """
    Create a pole vector constraint
    :param driver: str
    :param driven: str
    :param args: maintain shape_offset, etc
    :param kwargs: maintain shape_offset, etc
    :return: pole vector constraint
    """
    cns = cmds.poleVectorConstraint(driver,
                                    driven,
                                    name=format_constraint_name(driven, usageLib.pole_vector_constraint),
                                    *args, **kwargs)
    return cns[0]


def create_pole_with_matrices(driver, driven, start_joint):
    start_descriptor, start_side, start_usage = start_joint.split('_')
    start_usage_capitalize = '{}{}'.format(start_usage[0].upper(), start_usage[1:])

    driver_descriptor, driver_side, driver_usage = driver.split('_')

    start_point_mat_mult = cmds.createNode('pointMatrixMult', name='{}{}_{}_{}'.format(start_descriptor,
                                                                                       start_usage_capitalize,
                                                                                       start_side,
                                                                                       usageLib.point_matrix_mult))
    
    cmds.connectAttr('{}.parentMatrix'.format(start_joint), '{}.inMatrix'.format(start_point_mat_mult))
    cmds.connectAttr('{}.translate'.format(start_joint), '{}.inPoint'.format(start_point_mat_mult))

    start_point_compose = cmds.createNode('composeMatrix', name='{}{}_{}_{}'.format(start_descriptor,
                                                                                    start_usage_capitalize,
                                                                                    start_side,
                                                                                    usageLib.compose_matrix))

    cmds.connectAttr('{}.output'.format(start_point_mat_mult), '{}.inputTranslate'.format(start_point_compose))

    start_point_inverse_matrix = cmds.createNode('inverseMatrix', name='{}{}_{}_{}'.format(start_descriptor,
                                                                                           start_usage_capitalize,
                                                                                           start_side,
                                                                                           usageLib.inverse_matrix))

    cmds.connectAttr('{}.outputMatrix'.format(start_point_compose),
                     '{}.inputMatrix'.format(start_point_inverse_matrix))

    pole_vector_mult_mat = cmds.createNode('multMatrix', name='{}_{}_{}'.format(driver_descriptor,
                                                                                driver_side,
                                                                                usageLib.mult_matrix))

    cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.matrixIn[0]'.format(pole_vector_mult_mat))

    cmds.connectAttr('{}.outputMatrix'.format(start_point_inverse_matrix),
                     '{}.matrixIn[1]'.format(pole_vector_mult_mat))

    pole_vector_decompose = cmds.createNode('decomposeMatrix', name='{}_{}_{}'.format(driver_descriptor,
                                                                                      driver_side,
                                                                                      usageLib.decompose_matrix))

    cmds.connectAttr('{}.matrixSum'.format(pole_vector_mult_mat),
                     '{}.inputMatrix'.format(pole_vector_decompose))

    cmds.connectAttr('{}.outputTranslate'.format(pole_vector_decompose),
                     '{}.poleVector'.format(driven))


def connect_offset_parent_matrix(driver, driven,
                                 translate=True,
                                 rotate=True,
                                 scale=True,
                                 shear=True):
    """
    Connect worldMatrix from driven to the offsetParentMatrix of the driven
    :param translate: bool
    :param rotate: bool
    :param scale: bool
    :param shear: bool
    :param driver: str
    :param driven: str
    :return multMatrix node
    """
    if len(driven.split('_')) != 3:
        desc = driven
        side = sideLib.center
        usage = ''
        cmds.warning('Names must have 3 fields {descriptor}_{side}_{usage}')
    else:
        desc, side, usage = driven.split('_')

    # Get the difference between the two objects
    matrix_difference = mathLib.multiply_matrices_4_by_4(cmds.getAttr('{}.worldMatrix'.format(driven)),
                                                         cmds.getAttr('{}.worldInverseMatrix'.format(driver)))

    # Logic
    multmat = cmds.createNode('multMatrix', name='{}{}_{}_multmat'.format(desc, usage.capitalize(), side))
    cmds.setAttr('{}.matrixIn[0]'.format(multmat), matrix_difference, type='matrix')
    cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.matrixIn[1]'.format(multmat))

    if translate and rotate and scale and shear:
        cmds.connectAttr('{}.matrixSum'.format(multmat), '{}.offsetParentMatrix'.format(driven))
    else:
        pick_mat = cmds.createNode('pickMatrix', name='{}_{}_{}'.format(desc, side, usageLib.pick_matrix))
        cmds.connectAttr('{}.matrixSum'.format(multmat), '{}.inputMatrix'.format(pick_mat))

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
    return multmat


def connect_matrix_to_attribute(driver, driven_and_attr):
    """
    connect driver worldMatrix to an attribute, the result matrix will be the identity matrix
    :param driver: str
    :param driven_and_attr: str, e.g. rootOutputs_c_grp.root_c_ctr
    """
    node, attr = driven_and_attr.split('.')
    descriptor, side, usage = node.split('_')
    attr_capitalize = '{}{}'.format(attr[0].upper(), attr[1:])

    mult_matrix = cmds.createNode('multMatrix', name='{}{}_{}_{}'.format(descriptor,
                                                                         attr_capitalize,
                                                                         side,
                                                                         usageLib.mult_matrix))

    cmds.setAttr('{}.matrixIn[0]'.format(mult_matrix), cmds.getAttr('{}.worldInverseMatrix'.format(driver)),
                 type='matrix')
    cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.matrixIn[1]'.format(mult_matrix))

    cmds.connectAttr('{}.matrixSum'.format(mult_matrix), driven_and_attr)


def connect_matrix_from_attribute(driver_and_attr, driven):
    """
    connect an attribute to the offsetParentMatrix of the driven
    :param driver_and_attr: str, e.g. rootOutputs_c_grp.root_c_ctr
    :param driven: str
    """
    descriptor, side, usage = driven.split('_')
    mult_matrix = '{}{}_{}_{}'.format(descriptor, usage.capitalize(), side, usageLib.mult_matrix)

    if not cmds.objExists(mult_matrix):
        mult_matrix = cmds.createNode('multMatrix', name=mult_matrix)

    matrix_difference = mathLib.multiply_matrices_4_by_4(matrix_a=cmds.getAttr('{}.worldMatrix'.format(driven)),
                                                         matrix_b=mathLib.inverse_matrix(cmds.getAttr(driver_and_attr)))

    cmds.setAttr('{}.matrixIn[0]'.format(mult_matrix), matrix_difference, type='matrix')
    cmds.connectAttr(driver_and_attr, '{}.matrixIn[1]'.format(mult_matrix), force=True)

    if not cmds.isConnected('{}.matrixSum'.format(mult_matrix), '{}.offsetParentMatrix'.format(driven)):
        cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.offsetParentMatrix'.format(driven))

    for attr in 'trs':
        value = 0 if attr != 's' else 1
        for axis in 'xyz':
            if cmds.getAttr('{}.{}{}'.format(driven, attr, axis), settable=True):
                cmds.setAttr('{}.{}{}'.format(driven, attr, axis), value)


def transform_to_offset_parent_matrix(node, world_space=True, *args):
    """
    set matrix in the offsetParentMatrix and set transform to default
    :param node: str
    :param world_space: bool
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
            cmds.setAttr('{}.{}{}'.format(node, attr, axis), value)


def offset_parent_matrix_to_transform(node, world_space=True, *args):
    """
    set matrix in the transform and set offsetParentMatrix to default
    :param node: str
    :param world_space: bool
    """
    if not node:
        node = cmds.ls(selection=True)[0]

    if world_space:
        node_matrix = cmds.xform(node, query=True, worldSpace=True, matrix=True)
    else:
        node_matrix = cmds.xform(node, query=True, objectSpace=True, matrix=True)

    cmds.setAttr('{}.offsetParentMatrix'.format(node), mathLib.identity_matrix, type='matrix')

    if world_space:
        cmds.xform(node, worldSpace=True, matrix=node_matrix)
    else:
        cmds.xform(node, objectSpace=True, matrix=node_matrix)


def connect_point_matrix_mult_to_a_cv(driver, crv_and_cv):
    """
    connect only the position from a worldMatrix to a cv
    :param driver: str
    :param crv_and_cv: str, e.g. upArm_l_crvShape.cv[0]
    """
    crv = crv_and_cv.split('.')[0]
    cv = crv_and_cv.split('[')[-1].split(']')[0]

    descriptor = '{}Crv{}'.format(crv.split('_')[0], cv)
    side = crv_and_cv.split('_')[1]

    cv_pos = cmds.getAttr(crv_and_cv)[0]
    mult_matrix = cmds.createNode('multMatrix', name='{}_{}_{}'.format(descriptor, side, usageLib.mult_matrix))
    cmds.setAttr('{}.matrixIn[0]'.format(mult_matrix),
                 mathLib.multiply_matrices_4_by_4(matrix_b=cmds.getAttr('{}.worldInverseMatrix'.format(driver)),
                                                  matrix_a=[1, 0, 0, 0,
                                                            0, 1, 0, 0,
                                                            0, 0, 1, 0,
                                                            cv_pos[0], cv_pos[1], cv_pos[2], 1]),
                 type='matrix')
    cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.matrixIn[1]'.format(mult_matrix))

    point_matrix_mult = cmds.createNode('pointMatrixMult', name='{}_{}_{}'.format(descriptor,
                                                                                  side,
                                                                                  usageLib.point_matrix_mult))

    cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.inMatrix'.format(point_matrix_mult))

    cmds.connectAttr('{}.output'.format(point_matrix_mult), '{}.controlPoints[{}]'.format(crv, cv))


def create_uvpin(nurbs,
                 nodes):
    descriptor, side = nurbs.split('_')[:2]

    uvpin_node = cmds.createNode('uvPin', name='{}_{}_{}'.format(descriptor, side, usageLib.uvpin))

    # TODO: clean the normal and tangent axis set
    cmds.setAttr('{}.normalAxis'.format(uvpin_node), 1)
    cmds.setAttr('{}.tangentAxis'.format(uvpin_node), 0)
    cmds.setAttr('{}.normalAxis'.format(uvpin_node), 2)

    cmds.connectAttr('{}.worldSpace[0]'.format(nurbs), '{}.deformedGeometry'.format(uvpin_node))
    index = 0
    for node in nodes:
        transform_temp = cmds.createNode('transform')
        cmds.xform(transform_temp, worldSpace=True, matrix=cmds.xform(node, query=True, worldSpace=True, matrix=True))
        cpos_temp = cmds.createNode('closestPointOnSurface')

        cmds.connectAttr('{}.worldSpace[0]'.format(nurbs), '{}.inputSurface'.format(cpos_temp))
        cmds.connectAttr('{}.translate'.format(transform_temp), '{}.inPosition'.format(cpos_temp))

        u_value = cmds.getAttr('{}.parameterU'.format(cpos_temp))
        v_value = cmds.getAttr('{}.parameterV'.format(cpos_temp))

        cmds.connectAttr('{}.outputMatrix[{}]'.format(uvpin_node, index), '{}.offsetParentMatrix'.format(node))
        cmds.setAttr('{}.coordinate[{}].coordinateU'.format(uvpin_node, index), u_value)
        cmds.setAttr('{}.coordinate[{}].coordinateV'.format(uvpin_node, index), v_value)

        cmds.delete(transform_temp, cpos_temp)
        index += 1


def create_follow(base,
                  driver,
                  driven,
                  rot=False,
                  pos=False,
                  default_value=True):
    """
    create a follow, if rot or pos is True, the follow will be split
    :param base: str, node or node + Attribute
    :param driver: str, node or node + Attribute
    :param driven: str
    :param pos: bool
    :param rot: bool
    :param default_value: bool
    :return blendMatrix output
    """
    driven_descriptor, driven_side, driven_usage = driven.split('_')

    driven_matrix = cmds.xform(driven, query=True, worldSpace=True, matrix=True)
    #
    # base
    if '.' in base:
        base_descriptor = base.split('.')[-1].split('_')[0]
        base_capitalize_descriptor = '{}{}'.format(base_descriptor[0].upper(), base_descriptor[1:])
        base_output = base
        base_inverse_matrix = mathLib.inverse_matrix(cmds.getAttr(base))
    else:
        base_descriptor = base.split('_')[0]
        base_capitalize_descriptor = '{}{}'.format(base_descriptor[0].upper(), base_descriptor[1:])
        base_output = '{}.worldMatrix'.format(base)
        base_inverse_matrix = cmds.getAttr('{}.worldInverseMatrix'.format(driver))

    # base multmat
    base_mult_matrix = '{}{}_{}_{}'.format(driven_descriptor,
                                           base_capitalize_descriptor,
                                           driven_side,
                                           usageLib.mult_matrix)

    if not cmds.objExists(base_mult_matrix):
        base_mult_matrix = cmds.createNode('multMatrix', name=base_mult_matrix)
        cmds.connectAttr(base_output, '{}.matrixIn[1]'.format(base_mult_matrix))

    cmds.setAttr('{}.matrixIn[0]'.format(base_mult_matrix),
                 mathLib.multiply_matrices_4_by_4(matrix_a=driven_matrix, matrix_b=base_inverse_matrix), type='matrix')

    # driver
    if '.' in driver:
        driver_descriptor = driver.split('.')[-1].split('_')[0]
        driver_capitalize_descriptor = '{}{}'.format(driver_descriptor[0].upper(), driver_descriptor[1:])
        driver_output = driver
        driver_inverse_matrix = mathLib.inverse_matrix(cmds.getAttr(driver))
    else:
        driver_descriptor = driver.split('_')[0]
        driver_capitalize_descriptor = '{}{}'.format(driver_descriptor[0].upper(), driver_descriptor[1:])
        driver_output = '{}.worldMatrix'.format(driver)
        driver_inverse_matrix = cmds.getAttr('{}.worldInverseMatrix'.format(driver))

    # driver multmat
    driver_mult_matrix = cmds.createNode('multMatrix', name='{}{}_{}_{}'.format(driven_descriptor,
                                                                                driver_capitalize_descriptor,
                                                                                driven_side,
                                                                                usageLib.mult_matrix))
    cmds.setAttr('{}.matrixIn[0]'.format(driver_mult_matrix),
                 mathLib.multiply_matrices_4_by_4(matrix_a=driven_matrix,
                                                  matrix_b=driver_inverse_matrix), type='matrix')

    cmds.connectAttr(driver_output, '{}.matrixIn[1]'.format(driver_mult_matrix))

    # blendMatrix
    blend_matrix = '{}{}_{}_{}'.format(driven_descriptor,
                                       driven_usage.capitalize(),
                                       driven_side,
                                       usageLib.blend_matrix)
    if not cmds.objExists(blend_matrix):
        blend_matrix = cmds.createNode('blendMatrix', name=blend_matrix)

        cmds.connectAttr('{}.matrixSum'.format(base_mult_matrix), '{}.inputMatrix'.format(blend_matrix))

    target_index_list = cmds.ls('{}.target[*]'.format(blend_matrix))
    target_index = 0
    if len(target_index_list) != 0:
        target_index = int(max(target_index_list).split('[')[-1].split(']')[0]) + 1

    target_index = 'target[{}]'.format(target_index)

    cmds.connectAttr('{}.matrixSum'.format(driver_mult_matrix), '{}.{}.targetMatrix'.format(blend_matrix, target_index))

    # Delete old multMatrix
    mult_mat_connection = cmds.listConnections('{}.offsetParentMatrix'.format(driven))
    if mult_mat_connection:
        mult_mat_connection = [x for x in cmds.listConnections('{}.offsetParentMatrix'.format(driven))
                               if x.endswith(usageLib.mult_matrix)]
        if mult_mat_connection:
            cmds.delete(mult_mat_connection[0])

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
    driven_ah = attributeHelper.AttributeHelper(driven)
    driven_ah.add_separator_attribute(separator_name='Follows')
    if rot:
        attr_name = 'follow{}Rot'.format(driver_capitalize_descriptor)
        driven_ah.add_float_attribute(attr_name, minValue=0, maxValue=1, defaultValue=default_value)
        cmds.connectAttr('{}.{}'.format(driven, attr_name), '{}.{}.rotateWeight'.format(blend_matrix, target_index))

    if pos:
        attr_name = 'follow{}Pos'.format(driver_capitalize_descriptor)
        driven_ah.add_float_attribute(attr_name, minValue=0, maxValue=1, defaultValue=default_value)
        cmds.connectAttr('{}.{}'.format(driven, attr_name), '{}.{}.translateWeight'.format(blend_matrix, target_index))

    if not pos and not rot:
        attr_name = 'follow{}'.format(driver_capitalize_descriptor)
        driven_ah.add_float_attribute(attr_name, minValue=0, maxValue=1, defaultValue=default_value)
        cmds.connectAttr('{}.{}'.format(driven, attr_name), '{}.{}.translateWeight'.format(blend_matrix, target_index))
        cmds.connectAttr('{}.{}'.format(driven, attr_name), '{}.{}.rotateWeight'.format(blend_matrix, target_index))

    return blend_matrix


def export_connections(file_name, path):
    """
    Export nodes and connections to .mel file excluding the edge nodes
    :param file_name: str
    :param path: str
    """
    node_list = cmds.ls(sl=True)

    edge_connections_string = str()
    for node in node_list:
        inputs_list = cmds.listConnections(node, destination=False, plugs=True)
        if inputs_list:
            inputs_list = [x for x in inputs_list if x.split('.')[0] in node_list]
            inputs_list = [(x, cmds.listConnections(x, source=False, plugs=True)[0]) for x in inputs_list]
        outputs_list = cmds.listConnections(node, source=False, plugs=True)

        if outputs_list:
            outputs_list = [x for x in outputs_list if x.split('.')[0] in node_list]
            outputs_list = [(cmds.listConnections(x, destination=False, plugs=True)[0], x) for x in outputs_list]

        if not bool(inputs_list) or not bool(outputs_list):
            if bool(inputs_list):
                for input_value in inputs_list:
                    edge_connections_string += '\nconnectAttr "{}" "{}";'.format(input_value[0], input_value[1])

            if bool(outputs_list):
                for output_value in outputs_list:
                    edge_connections_string += '\nconnectAttr "{}" "{}";'.format(output_value[0], output_value[1])

            cmds.select(node, deselect=True)

    if os.path.exists(r'{}\{}.ma'.format(path, file_name)):
        os.remove(r'{}\{}.ma'.format(path, file_name))

    cmds.file(r'{}\{}.ma'.format(path, file_name), type='mayaAscii', exportSelectedStrict=True, force=True)

    os.replace(r'{}\{}.ma'.format(path, file_name), r'{}\{}.mel'.format(path, file_name))

    with open(r'{}\{}.mel'.format(path, file_name), 'r+') as connections_file:
        # Read and store all lines into list
        lines = connections_file.readlines()

        # Move file pointer to the beginning of a file
        connections_file.seek(0)

        # empty the file
        connections_file.truncate()

        # ----- Lines to keep in the file -----
        # Get lines that are not indented (createNode, connectNode, sceneInfo, selects)
        no_indented_line_list = [index for index, value in enumerate(lines) if not value.startswith('\t')]

        # Get the lines with createNode or connectAttr
        main_line_list = [index for index, value in enumerate(lines) if
                          value.startswith('createNode') or value.startswith('connectAttr')]

        # Create ranges between a main line and the next non-indented line
        # This range is to store the setAttr lines of that createNode
        range_list = [(value, no_indented_line_list[no_indented_line_list.index(value) + 1]) for index, value in
                      enumerate(main_line_list) if value in no_indented_line_list if value != main_line_list[-1]]

        # Store all the lines that we want to export
        lines_to_write = [x for sublist in
                          [[x for x in range(start_index, end_index)] for start_index, end_index in range_list] for x in
                          sublist]

        # Write lines to the file
        for index in lines_to_write:
            if 'rename' not in lines[index]:
                connections_file.writelines(lines[index])

        # Write edge connections
        if len(edge_connections_string) != 0:
            connections_file.write(edge_connections_string)

    cmds.select(node_list)

    print(end='\n')
    print(end=r'{}/{}.mel has been exported'.format(path, file_name))


def import_connections(path):
    """
    Import connections from mel file
    """
    #  TODO if a node exists don't create it
    cmds.file(path, i=True)  # i = import

    print(end='\n')
    print(end=r'{} has been imported'.format(path))
