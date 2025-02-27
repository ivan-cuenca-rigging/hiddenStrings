# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import math_lib, side_lib, usage_lib, node_lib, import_export_lib

colors_dict = {'default': 0,
               'black': 1,
               'gray': 2,
               'lightGray': 3,
               'crimson': 4,
               'darkBlue': 5,
               'blue': 6,
               'left': 6,
               side_lib.left: 6,
               'darkGreen': 7,
               'darkPurple': 8,
               'pink': 9,
               'brownLight': 10,
               'brown': 11,
               'darkOrange': 12,
               'red': 13,
               'right': 13,
               side_lib.right: 13,
               'green': 14,
               'blue2': 15,
               'white': 16,
               'yellow': 17,
               'center': 17,
               side_lib.center: 17,
               'lightBlue': 18,
               'lightGreen': 19,
               'lightPink': 20,
               'lightOrange': 21,
               'lightYellow': 22,
               'green2': 23,
               'brown2': 24,
               'pistachio': 25,
               'green3': 26,
               'green4': 27,
               'turquoise': 28,
               'blue3': 29,
               'purple': 30,
               'darkPink': 31}


def get_spl_data(spl):
    """
    Get the spline data
    
    Args:
        spl (str): spline
    
    Returns:
        dict: spline data
    """
    crv_list = cmds.listRelatives(spl, shapes=True)
    spline_data = dict()
    for crv in crv_list:
        spline_data[crv] = dict()
        crv_degree = cmds.getAttr(f'{crv}.degree')
        crv_per = cmds.getAttr(f'{crv}.form')
        crv_cvs = cmds.ls(f'{crv}.cv[*]', flatten=True)
        cvs_pos = list()
        for cv in crv_cvs:
            cv_pos = cmds.xform(cv, query=True, worldSpace=True, translation=True)
            cvs_pos.append(cv_pos)

        spline_data[crv]['periodic'] = False
        if crv_per == 2:
            crv_knot = []
            for index in range(crv_degree):
                cvs_pos.append(cvs_pos[index])
                crv_knot = [i for i in range(len(cvs_pos) + crv_degree - 1)]

            spline_data[crv]['periodic'] = True
            spline_data[crv]['knot'] = crv_knot

        spline_data[crv]['degree'] = crv_degree
        spline_data[crv]['point'] = cvs_pos

    return spline_data


def create_spl_from_data(spl_name, spl_data, spl_scale=1):
    """
    Create a spline with the data given

    Args:
        spl_name (str): spline name
        spl_data (dict): spline data
        spl_scale (float): spline scale

    Returns:
        str: spline
    """
    spline = cmds.createNode('transform', name=spl_name)
    for crv in spl_data:
        crv = cmds.curve(**spl_data[crv])  # ** to pass dictionary key-values as arguments

        crv_shapes = cmds.listRelatives(crv, shapes=True)[0]
        cmds.parent(crv_shapes, spline, relative=True, shape=True)
        cmds.delete(crv)
    crv_shapes = cmds.listRelatives(spline, children=True)
    for i, shp in enumerate(crv_shapes):
        shp = cmds.rename(shp, f'{spline}Shape{i + 1}')
        cmds.scale(spl_scale, spl_scale, spl_scale, cmds.select(f'{shp}.cv[*]'), r=True, ocp=True)
    cmds.select(spline)
    return spline


def delete_shapes(node):
    """
    Delete the node's shapes

    Args:
        node (str): node's name
    """
    shapes_list = cmds.listRelatives(node, children=True, shapes=True)
    if shapes_list:
        cmds.delete(shapes_list)


def get_shapes(node):
    """
    Get node's shapes

    Args:
        node (str): node's name

    Returns:
        list: node's shapes
    """
    return cmds.listRelatives(node, children=True, shapes=True)


def set_shape(node, shape_name, shape_scale=1, shape_offset=None):
    """
    Set node's shape

    Args:
        node (str): node's name
        shape_name (str): from spline_shapes
        shape_scale (float): scale of the shape. Defaults to 1.
        shape_offset (dict):, E.G. {'translateY': 1}. Defaults to 1.
    """
    temp_spl = create_spl_from_data('temp_c_spl',
                                    spl_data=import_export_lib.import_data_from_json(file_name=shape_name,
                                                                                     file_path='libs/spline_shapes'),
                                    spl_scale=shape_scale)
    if shape_offset:
        for key, value in shape_offset.items():
            cmds.setAttr(f'{temp_spl}.{key}', value)
    replace_shape(node=node, shape_transform=temp_spl)


def replace_shape(node, shape_transform, keep_shapes=False):
    """
    Replace the node's shapes

    Args:
        node (str): node's name
        shape_transform (str): shape transform
        keep_shapes (bool): True == new shape will be added instead of replacing the existings one. Defaults to False

    Returns:
        list: new shapes list
    """
    if not keep_shapes:
        delete_shapes(node)

    if cmds.listRelatives(shape_transform, parent=True) != [node]:
        cmds.parent(shape_transform, node)

    for cns_type in ['parentConstraint', 'pointConstraint', 'orientConstraint',
                     'aimConstraint', 'poleVectorConstraint', 'scaleConstraint']:
        cns_list = cmds.listRelatives(shape_transform, type=cns_type)
        if cns_list:
            cmds.delete(cns_list)

    cmds.makeIdentity(shape_transform, apply=True, translate=True, rotate=True,
                      scale=True, normal=0, preserveNormals=True)

    shapes_list = cmds.listRelatives(shape_transform, children=True, shapes=True)

    for index, shape in enumerate(shapes_list):
        cmds.parent(shape, node, relative=True, shape=True)
        index = '' if shape == shapes_list[0] else index
        cmds.rename(shape, f"{node}Shape{index}")

    cmds.delete(shape_transform)

    return cmds.listRelatives(node, shapes=True, fullPath=True)


def transfer_shape(source, target):
    """
    Transfer shape from source to target

    Args:
        source (str): source node
        target (str): target node
    """
    # Get spline shape
    spline_data = get_spl_data(spl=source)
    # Get spline color
    spline_color = get_override_color(target)

    # Create a temporal transform in the source position
    spline_transform = cmds.createNode('transform', name=f'{target}Spl')
    cmds.xform(spline_transform, worldSpace=True, matrix=cmds.xform(source, query=True, worldSpace=True, matrix=True))

    # Create the spline and transfer it to the temporal transform
    spline = create_spl_from_data(spl_name=f'{target}Spl', spl_data=spline_data)
    replace_shape(node=spline_transform, shape_transform=spline, keep_shapes=False)

    # Place the shape in the target position
    cmds.xform(spline_transform, worldSpace=True, matrix=cmds.xform(target, query=True, worldSpace=True, matrix=True))

    # Transfer the shape to the target
    replace_shape(node=target, shape_transform=spline_transform, keep_shapes=False)
    if spline_color:
        set_override_color(splines_list=[target], color_key=spline_color)


def set_override_color(splines_list=None, color_key='red'):
    """
    override the spline color

    Args:
        splines_list (list): list of splines
        color_key (str): check valid color keys in the spline_lib
    """
    if not splines_list:
        splines_list = cmds.ls(sl=True)

    color_value = 0
    if isinstance(color_key, int):
        if 1 <= color_key <= 31:
            color_value = color_key
        else:
            cmds.error(f'{color_key} is out of range of 1 - 31')
    else:
        if color_key in colors_dict.keys():
            color_value = colors_dict[color_key]
        else:
            cmds.error(f'{color_key} is not a valid color, try any of these: {list(colors_dict.keys())}')

    override_value = 0 if color_value == 0 else 1
    for spl in splines_list:
        spl_shapes = cmds.listRelatives(spl, shapes=True)
        for spl_shape in spl_shapes:
            cmds.setAttr(f'{spl_shape}.overrideEnabled', override_value)
            cmds.setAttr(f'{spl_shape}.overrideRGBColors', 0)
            cmds.setAttr(f'{spl_shape}.overrideColor', color_value)


def get_override_color(spl):
    """
    Get the override attribute value

    Args:
        spl (str): name of the spline

    Returns:
        int: spline.overrideColor value
    """
    spl_shape = cmds.listRelatives(spl, shapes=True)[0]
    return cmds.getAttr(f'{spl_shape}.overrideColor')


def create_curve_from_a_to_b(name, a, b, n, degree=3):
    """
    Create a spline curve from a to b

    Args:
        name (str): name of the new spline
        a (str): name of the a node
        b (str): name of the b node
        n (_type_): number of control vertex
        degree (int, optional): degree of the spline. Defaults to 3.

    Returns:
        str: spline's name
    """
    cvs_pos_lists = list(math_lib.get_n_positions_from_a_to_b(a, b, n))
    return cmds.curve(p=cvs_pos_lists, name=name, degree=degree)


def attach_curve_from_a_to_b(a, b):
    """
    Create a spline with two controls points, one attached to a and another attached to b

    Args:
        a (str): a node's name
        b (str): b node's name

    Returns:
        str: spline
    """
    a_nh = node_lib.Helper(a)
    b_nh = node_lib.Helper(b)

    spl = create_curve_from_a_to_b('temp', a, b, 2, degree=1)
    cmds.setAttr(f'{cmds.listRelatives(spl, shapes=True)[0]}.template', 1)
    spl = replace_shape(node=a, shape_transform=spl, keep_shapes=True)[-1]

    b_pmatmult = cmds.createNode('pointMatrixMult', name='{}_{}_{}'.format(b_nh.get_descriptor(),
                                                                           b_nh.get_side(),
                                                                           usage_lib.point_matrix_mult))
    a_pmatmult = cmds.createNode('pointMatrixMult', name='{}{}_{}_{}'.format(a_nh.get_descriptor(),
                                                                             b_nh.get_descriptor_capitalize(),
                                                                             a_nh.get_side(),
                                                                             usage_lib.point_matrix_mult))

    cmds.connectAttr(f'{b}.worldMatrix', f'{b_pmatmult}.inMatrix')
    cmds.connectAttr(f'{a}.worldInverseMatrix', f'{a_pmatmult}.inMatrix')

    for axis in ['X', 'Y', 'Z']:
        cmds.connectAttr(f'{b_pmatmult}.output{axis}', f'{a_pmatmult}.inPoint{axis}')

        cmds.connectAttr(f'{a_pmatmult}.output{axis}', '{}.controlPoints[1].{}Value'.format(spl,
                                                                                                      axis.lower()))

    return spl
