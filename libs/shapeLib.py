# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import mathLib, sideLib, jsonLib, usageLib
from hiddenStrings.libs.helpers import nodeHelper


colors_dict = {'default': 0,
               'black': 1,
               'gray': 2,
               'lightGray': 3,
               'crimson': 4,
               'darkBlue': 5,
               'blue': 6,
               'left': 6,
               sideLib.left: 6,
               'darkGreen': 7,
               'darkPurple': 8,
               'pink': 9,
               'brownLight': 10,
               'brown': 11,
               'darkOrange': 12,
               'red': 13,
               'right': 13,
               sideLib.right: 13,
               'green': 14,
               'blue2': 15,
               'white': 16,
               'yellow': 17,
               'center': 17,
               sideLib.center: 17,
               'lightBlue': 18,
               'lightGreen': 19,
               'lightPink': 20,
               'lightOrange': 21,
               'lightYellow': 22,
               'green2': 23,
               'brown2': 24,
               'pistache': 25,
               'green3': 26,
               'green4': 27,
               'turquoise': 28,
               'blue3': 29,
               'purple': 30,
               'darkPink': 31}


def get_spl_data(spl):
    """
    Get the spline data
    :param spl: str
    :return: spline data
    """
    crv_list = cmds.listRelatives(spl, shapes=True)
    output_dict = dict()
    for crv in crv_list:
        output_dict[crv] = dict()
        crv_degree = cmds.getAttr('{}.degree'.format(crv))
        crv_per = cmds.getAttr('{}.form'.format(crv))
        crv_cvs = cmds.ls('{}.cv[*]'.format(crv), flatten=True)
        cvs_pos = list()
        for cv in crv_cvs:
            cv_pos = cmds.xform(cv, query=True, worldSpace=True, translation=True)
            cvs_pos.append(cv_pos)

        output_dict[crv]['periodic'] = False
        if crv_per == 2:
            crv_knot = []
            for index in range(crv_degree):
                cvs_pos.append(cvs_pos[index])
                crv_knot = [i for i in range(len(cvs_pos) + crv_degree - 1)]

            output_dict[crv]['periodic'] = True
            output_dict[crv]['knot'] = crv_knot

        output_dict[crv]['degree'] = crv_degree
        output_dict[crv]['point'] = cvs_pos

    return output_dict


def create_spl_from_data(spl_name, spl_data, spl_scale=1):
    """
    Create a spline with the data given
    :param spl_name: str
    :param spl_data: dict
    :param spl_scale: float
    :return: spline
    """
    spl = cmds.createNode('transform', name=spl_name)
    for crv in spl_data:
        crv = cmds.curve(**spl_data[crv])
        crv_shapes = cmds.listRelatives(crv, shapes=True)[0]
        cmds.parent(crv_shapes, spl, relative=True, shape=True)
        cmds.delete(crv)
    crv_shapes = cmds.listRelatives(spl, children=True)
    for i, shp in enumerate(crv_shapes):
        shp = cmds.rename(shp, '{}Shape{}'.format(spl, i + 1))
        cmds.scale(spl_scale, spl_scale, spl_scale, cmds.select('{}.cv[*]'.format(shp)), r=True, ocp=True)
    cmds.select(spl)
    return spl


def delete_shapes(node):
    """
    Delete the node's shapes
    :param node: str
    """
    shapes_list = cmds.listRelatives(node, children=True, shapes=True)
    if shapes_list:
        cmds.delete(shapes_list)


def get_shapes(node):
    """
    Get node's shapes
    :param node: str
    :return: node's shapes
    """
    return cmds.listRelatives(node, children=True, shapes=True)


def set_shape(node, shape_name, shape_scale=1, shape_offset=None):
    """
    Set node's shape
    :param node: str
    :param shape_name: str, from libs/shapes
    :param shape_scale: float
    :param shape_offset: dict, E.g. offset=dict(); offset['translateY'] = 1
    """
    temp_spl = create_spl_from_data('temp_c_spl', spl_data=jsonLib.import_data_from_json(file_name=shape_name,
                                                                                         file_path='libs/shapes'),
                                    spl_scale=shape_scale)
    if shape_offset:
        for key, value in shape_offset.items():
            cmds.setAttr('{}.{}'.format(temp_spl, key), value)
    replace_shape(node=node, shape_transform=temp_spl)


def replace_shape(node, shape_transform, keep_shapes=False):
    """
    Replace the node's shapes
    :param node: str
    :param shape_transform: str
    :param keep_shapes: bool
    :return: new shape
    """
    ctr_nh = nodeHelper.NodeHelper(node)
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
    new_shape_list = []
    for shp in shapes_list:
        cmds.parent(shp, node, relative=True, shape=True)
        shp = cmds.rename(shp, '{}Shape'.format(ctr_nh))
        new_shape_list.append(shp)

    cmds.delete(shape_transform)
    return new_shape_list


def override_color(splines_list=None, color_key='red'):
    """
    override the spline color
    :param splines_list: list
    :param color_key: str, check valid color keys
    """
    if not splines_list:
        splines_list = cmds.ls(sl=True)

    color_value = 0
    if isinstance(color_key, int):
        if 1 <= color_key <= 31:
            color_value = color_key
        else:
            cmds.error('{} is out of range of 1 - 31'.format(color_key))
    else:
        if color_key in colors_dict.keys():
            color_value = colors_dict[color_key]
        else:
            cmds.error('{} is not a valid color, try any of these: {}'.format(color_key, list(colors_dict.keys())))

    override_value = 0 if color_value == 0 else 1
    for spl in splines_list:
        spl_shapes = cmds.listRelatives(spl, shapes=True)
        for spl_shape in spl_shapes:
            cmds.setAttr('{}.overrideEnabled'.format(spl_shape), override_value)
            cmds.setAttr('{}.overrideRGBColors'.format(spl_shape), 0)
            cmds.setAttr('{}.overrideColor'.format(spl_shape), color_value)


def create_curve_from_a_to_b(name, a, b, n, d=3):
    cvs_pos_lists = list(mathLib.get_n_positions_from_a_to_b(a, b, n))
    return cmds.curve(p=cvs_pos_lists, name=name, degree=d)


def attach_curve_from_a_to_b(a, b):
    a_nh = nodeHelper.NodeHelper(a)
    b_nh = nodeHelper.NodeHelper(b)

    spl = create_curve_from_a_to_b('temp', a, b, 2, d=1)
    cmds.setAttr('{}.template'.format(cmds.listRelatives(spl, shapes=True)[0]), 1)
    spl = replace_shape(node=a, shape_transform=spl, keep_shapes=True)[0]
    b_pmatmult = cmds.createNode('pointMatrixMult', name='{}_{}_{}'.format(b_nh.get_descriptor(),
                                                                           b_nh.get_side(),
                                                                           usageLib.point_matrix_mult))
    a_pmatmult = cmds.createNode('pointMatrixMult', name='{}{}_{}_{}'.format(a_nh.get_descriptor(),
                                                                             b_nh.get_descriptor_capitalize(),
                                                                             a_nh.get_side(),
                                                                             usageLib.point_matrix_mult))

    cmds.connectAttr('{}.worldMatrix'.format(b), '{}.inMatrix'.format(b_pmatmult))
    cmds.connectAttr('{}.output'.format(b_pmatmult), '{}.inPoint'.format(a_pmatmult))
    cmds.connectAttr('{}.worldInverseMatrix'.format(a), '{}.inMatrix'.format(a_pmatmult))

    for axis in ['X', 'Y', 'Z']:
        cmds.connectAttr('{}.output{}'.format(a_pmatmult, axis),
                         '{}.controlPoints[1].{}Value'.format(spl, axis.lower()))

    return spl
