# Imports
from collections import OrderedDict

# Maya imports
from maya import cmds, mel

# Project imports
from hiddenStrings.libs import side_lib, usage_lib, node_lib


def check_blendshape(blend_shape):
    """
    Check if the blendShape node exists and if it is a blendShape
    :param blend_shape: str
    """
    if not cmds.objExists(blend_shape):
        cmds.error('{} does not exists in the scene'.format(blend_shape))
    if cmds.objectType(blend_shape) != 'blendShape':
        cmds.error('{} is not a blendShape'.format(blend_shape))


def check_target(blend_shape, target):
    """
    Check if the blendS shape target already exists
    :param blend_shape: str
    :param target: str
    :return: bool
    """
    check_blendshape(blend_shape=blend_shape)

    targets_list = cmds.listAttr('{}.weight'.format(blend_shape), multi=True)
    if targets_list and target in targets_list:
        return True
    else:
        return False


def check_in_between(blend_shape, target, value):
    """
    Check if the blendS shape target in-between already exists
    :param blend_shape: str
    :param target: str
    :param value: float
    :return: bool
    """
    target_index = get_target_index(blend_shape=blend_shape, target=target)
    target_data = cmds.listAttr('{}.inputTarget[0].inputTargetGroup[{}]'.format(blend_shape, target_index), multi=True)

    target_values_list = list()
    for target in target_data:
        if target.find("inputGeomTarget") != -1:
            target_value = target.split('.')[-2].split('[')[-1].split(']')[0]

            target_value = (int(target_value) - 5000) * 0.001
            target_values_list.append(target_value)

    if value in target_values_list:
        return True
    else:
        return False


def get_blend_shape_name(node):
    """
    Format the blend_shape_name
    :param node: str
    :return: blendShape name
    """
    if len(node.split('_')) != 3:
        return '{}_{}'.format(node, usage_lib.blend_shape)
    else:
        descriptor, side, usage = node.split('_')
        return '{}{}_{}_{}'.format(descriptor, usage.capitalize(),
                                   side,
                                   usage_lib.blend_shape)


def get_blend_shape(node):
    """
    Find blendShape attached to the node
    :param node: str
    :return: blendshape
    """
    blend_shape = None
    inputs_list = cmds.listHistory(node, interestLevel=1, pruneDagObjects=True)
    if inputs_list:
        for item in inputs_list:
            if cmds.objectType(item) == 'blendShape':
                blend_shape = item
    return blend_shape


def get_blend_shape_node(blend_shape):
    """
    Get the node deformed by the blendShape
    :param blend_shape: str
    :return: node
    """
    node_shape = cmds.blendShape(blend_shape, query=True, geometry=True)[0]
    node = cmds.listRelatives(node_shape, parent=True)[0]
    return node


def get_blend_shape_index(blend_shape):
    """
    Get the blendShape index
    :param blend_shape: string
    return index
    """
    return cmds.listConnections('{}.midLayerParent'.format(blend_shape), plugs=True)[0].split('[')[-1].split(']')[0]


def get_target_name(blend_shape, target_index):
    """
    Get the target's name
    :param blend_shape: str
    :param target_index: int
    :return: target name
    """
    return cmds.listAttr('{}.weight[{}]'.format(blend_shape, target_index))[0]


def get_targets_from_shape_editor(as_index=True):
    """
    Get targets from the shape editor
    :param as_index: bool
    return target list as_index -> [blendShape1.0, blendShape1.1, ...] not as_index [blendShape1.target, ...]
    """
    selection_list = mel.eval('getShapeEditorTreeviewSelection(24)')
    if not as_index:
        selection_list = ['{}.{}'.format(x.split('.')[0],
                                         get_target_name(blend_shape=x.split('.')[0],
                                                         target_index=x.split('.')[1])) for x in selection_list]

    return selection_list


def get_target_values(blend_shape, target):
    """
    Get the values of the in-betweens of a target (include the 1.0 value)
    :param blend_shape: str
    :param target: str
    :return: target values list
    """
    check_blendshape(blend_shape=blend_shape)

    target_index = get_target_index(blend_shape=blend_shape, target=target)
    target_data = cmds.listAttr('{}.inputTarget[0].inputTargetGroup[{}]'.format(blend_shape, target_index), multi=True)

    target_values_list = list()
    for target in target_data:
        if target.find("inputGeomTarget") != -1:
            target_value = target.split('.')[-2].split('[')[-1].split(']')[0]

            target_value = (int(target_value) - 5000) * 0.001
            target_values_list.append(target_value)

    return target_values_list


def get_target_index(blend_shape, target):
    """
    Get the last index of a blendshape
    :param blend_shape: str
    :param target: str
    """
    check_blendshape(blend_shape=blend_shape)

    targets_list = cmds.listAttr('{}.weight'.format(blend_shape), multi=True)
    if targets_list and target in targets_list:
        return targets_list.index(target)
    else:
        return None


def get_next_target_index(blend_shape):
    """
    Get the next target index of a blendshape
    :param blend_shape: str
    """
    check_blendshape(blend_shape=blend_shape)

    if cmds.listAttr('{}.weight'.format(blend_shape), multi=True):
        index = len(cmds.listAttr('{}.weight'.format(blend_shape), multi=True))
    else:
        index = 0

    return int(index)


def get_blend_shapes_from_shape_editor():
    """
    Get blendShapes from the shape editor
    return blendShape list [blendShape1, blendShape2, ...]
    """
    return mel.eval('getShapeEditorTreeviewSelection(11)')


def get_in_betweens_from_shape_editor():
    """
    Get in-between targets from the shape editor
    return target list [blendShape1.0.5, blendShape1.0.3, ...]
    """
    return mel.eval('getShapeEditorTreeviewSelection(16)')


def get_blend_shape_data(blend_shape):
    """
    Get blendshape data, including target in-between values and deltas
    :param blend_shape: str
    :return: blend_shape_data
    """
    check_blendshape(blend_shape=blend_shape)

    blend_shape_data = OrderedDict()

    blend_shape_data['node'] = get_blend_shape_node(blend_shape)
    blend_shape_data['blendShape'] = blend_shape
    blend_shape_data['targets'] = dict()

    targets_order_list = cmds.getAttr('{}.targetDirectory[0].childIndices'.format(blend_shape))
    for target_order in targets_order_list:
        target = get_target_name(blend_shape=blend_shape, target_index=target_order)

        blend_shape_data['targets'][target] = get_target_data(blend_shape=blend_shape, target=target)

    return blend_shape_data


def get_target_data(blend_shape, target):
    """
    Get target data, including in-betweens values and deltas
    :param blend_shape: str
    :param target: str
    :return: target_data
    """
    target_dict = dict()

    target_dict['envelope'] = round(cmds.getAttr('{}.{}'.format(blend_shape, target)), 3)

    target_dict['target_values'] = dict()
    target_value_list = get_target_values(blend_shape=blend_shape, target=target)
    for target_value in target_value_list:
        target_value = round(target_value, 3)
        target_value_int = int(target_value * 1000 + 5000)
        target_value = str(round(target_value, 3))
        points_target = cmds.getAttr(
            '{}.inputTarget[0].inputTargetGroup[{}].inputTargetItem[{}].inputPointsTarget'.format(
                blend_shape,
                get_target_index(blend_shape=blend_shape, target=target),
                target_value_int))

        component_target = cmds.getAttr(
            '{}.inputTarget[0].inputTargetGroup[{}].inputTargetItem[{}].inputComponentsTarget'.format(
                blend_shape,
                get_target_index(blend_shape=blend_shape, target=target),
                target_value_int))

        target_data = dict()
        target_data['inputPointsTarget'] = points_target
        target_data['inputComponentsTarget'] = component_target

        target_dict['target_values'][target_value] = target_data

    return target_dict


def set_blendshape_data(blend_shape, blend_shape_data):
    """
    set blendShape data including targets, in-betweens values and deltas
    :param blend_shape: str
    :param blend_shape_data: dict
    """
    for target in blend_shape_data['targets']:
        set_target_data(blend_shape=blend_shape, target=target, target_data=blend_shape_data['targets'][target])


def set_target_data(blend_shape, target, target_data):
    """
    set target data including in-betweens values and deltas
    :param blend_shape: str
    :param target: str
    :param target_data: dict
    """
    if not check_target(blend_shape=blend_shape, target=target):
        add_target(blend_shape=blend_shape, target=target)

    target_index = get_target_index(blend_shape=blend_shape, target=target)
    for target_value in target_data['target_values']:
        points_target = target_data['target_values'][target_value]['inputPointsTarget']
        components_target = target_data['target_values'][target_value]['inputComponentsTarget']
        pretty_target_value = target_value
        target_value = int(float(target_value) * 1000 + 5000)

        if target_value != 6000 and not check_in_between(blend_shape=blend_shape,
                                                         target=target,
                                                         value=target_value):
            add_in_between(blend_shape=blend_shape,
                           existing_target=target,
                           in_between_target='{}_{}'.format(target, pretty_target_value),
                           value=pretty_target_value)

        if points_target and components_target:
            cmds.setAttr('{}.inputTarget[0].inputTargetGroup[{}].inputTargetItem[{}].inputPointsTarget'.format(
                blend_shape,
                target_index,
                target_value),
                len(points_target),
                *points_target,
                type='pointArray')
            cmds.setAttr('{}.inputTarget[0].inputTargetGroup[{}].inputTargetItem[{}].inputComponentsTarget'.format(
                blend_shape,
                target_index,
                target_value),
                len(components_target),
                *components_target,
                type='componentList')

        if target_value != 6000:
            cmds.setAttr('{}.inbetweenInfoGroup[{}].inbetweenInfo[{}].inbetweenTargetName'.format(blend_shape,
                                                                                                  target_index,
                                                                                                  target_value),
                         '{}_{}'.format(target, pretty_target_value),
                         type='string')

        cmds.setAttr('{}.{}'.format(blend_shape, target), target_data['envelope'])


def rename_blend_shape(blend_shape):
    """
    Rename blendShape name
    :param blend_shape: str
    :return: blendShape name
    """
    node_shape = cmds.blendShape(blend_shape, query=True, geometry=True)[0]
    node = cmds.listRelatives(node_shape, parent=True)[0]

    return cmds.rename(blend_shape, get_blend_shape_name(node))


def rename_all_blend_shapes():
    """
    Rename all the blendShapes in the scene
    """
    blend_shape_list = cmds.ls(type='blendShape')
    for blend_shape in blend_shape_list:
        rename_blend_shape(blend_shape)


def create_blend_shape(node, target_list=None):
    """
    create a blendShape
    :param node: str, geometry, nurbs, curve, etc
    :param target_list: list, if None it will create a blendshape without targets
    :return: blendShape
    """
    blend_shape = cmds.blendShape(node, topologyCheck=False, name=get_blend_shape_name(node))[0]
    if target_list:
        for target in target_list:
            add_target(blend_shape=blend_shape, target=target)

    return blend_shape


def add_target(blend_shape, target):
    """
    Add target to an existing blendShape
    :param blend_shape: str
    :param target: str
    :return: target
    """
    check_blendshape(blend_shape=blend_shape)
    node = get_blend_shape_node(blend_shape=blend_shape)
    index = get_next_target_index(blend_shape=blend_shape)

    if cmds.objExists(target):
        cmds.blendShape(blend_shape, edit=True, topologyCheck=False, target=(node, index, target, 1.0))
    else:
        target = cmds.duplicate(node, name=target)[0]
        cmds.blendShape(blend_shape, edit=True, topologyCheck=False, target=(node, index, target, 1.0))

        cmds.delete(target)

        cmds.blendShape(blend_shape, edit=True, resetTargetDelta=(0, get_target_index(blend_shape=blend_shape,
                                                                                      target=target)))

    return target


def add_in_between(blend_shape, existing_target, in_between_target, value):
    """
    Add target to an existing blendShape
    :param blend_shape: str
    :param in_between_target: str
    :param value: float, 0 to 1
    :param existing_target: str
    """
    check_blendshape(blend_shape=blend_shape)
    value = float(value)
    if not 0.0 < value < 1.0:
        cmds.error('The in-between must have a value greater than 0 but lower than 1')

    node_shape = cmds.blendShape(blend_shape, query=True, geometry=True)[0]
    node = cmds.listRelatives(node_shape, parent=True)[0]
    index = get_target_index(blend_shape=blend_shape, target=existing_target)

    if cmds.objExists(in_between_target):
        cmds.blendShape(blend_shape, edit=True, topologyCheck=False, target=(node, index, in_between_target, value))
    else:
        in_between_target = cmds.duplicate(node, name=existing_target)[0]
        cmds.blendShape(blend_shape, edit=True, topologyCheck=False, target=(node, index, in_between_target, value))
        cmds.delete(in_between_target)


def remove_target(blend_shape, target):
    """
    Remove target from an existing blendShape
    :param blend_shape: str
    :param target: str
    """
    check_blendshape(blend_shape=blend_shape)

    index = get_target_index(blend_shape=blend_shape, target=target)

    mel.eval('blendShapeDeleteTargetGroup {} {}'.format(blend_shape, index))


def remove_in_between(blend_shape, target, value):
    """
    Remove in-between from an existing target
    :param blend_shape: str
    :param target: str
    :param value: float
    """
    check_blendshape(blend_shape=blend_shape)

    index = get_target_index(blend_shape=blend_shape, target=target)

    if check_in_between(blend_shape=blend_shape, target=target, value=value):
        value = float(value)
        value = value * 1000 + 5000

        mel.eval('blendShapeDeleteInBetweenTarget {} {} {}'.format(blend_shape, index, value))
    else:
        cmds.error('the in-between at {} does not exists in {}.{}'.format(value, blend_shape, target))


def edit_target_or_in_between(*args):
    """
    Set on edit a target or an in-between target even when there is a direct connection
    """
    inbetween_shape_editor_values = get_in_betweens_from_shape_editor()
    if inbetween_shape_editor_values:
        blendshape_node, target_index, inbetween_index = inbetween_shape_editor_values[0].split('.')

        inbetween_value = (float(inbetween_index) / 1000.0) - 5

        cmds.sculptTarget(blendshape_node, edit=True, target=int(target_index), inbetweenWeight=inbetween_value)

    else:
        target_shape_editor_values = get_targets_from_shape_editor()
        if target_shape_editor_values:
            blendshape_node, target_index = target_shape_editor_values[0].split('.')
            cmds.sculptTarget(blendshape_node, edit=True, target=int(target_index))


def mirror_target(blend_shape, target):
    """
    Mirror blendShape target (It only works with geometries for now)
    :param blend_shape: str
    :param target: str
    """
    # Get mirror target name
    if len(target.split('_')) == 3:
        descriptor, side, usage = target.split('_')
    else:
        descriptor = target
        side = side_lib.left
        usage = usage_lib.corrective
    mirror_target_name = '{}_{}_{}'.format(descriptor, side_lib.get_opposite_side(side), usage)

    # Get target data
    target_data = get_target_data(blend_shape=blend_shape, target=target)

    # Set target data in the mirror target
    set_target_data(blend_shape=blend_shape, target=mirror_target_name, target_data=target_data)

    # Mirror target
    get_symmetry = cmds.symmetricModelling(query=True, symmetry=True)
    target_index = get_target_index(blend_shape, mirror_target_name)
    cmds.blendShape(blend_shape, edit=True, symmetryAxis='x', symmetrySpace=1, flipTarget=[0, target_index])
    if get_symmetry:
        cmds.symmetricModelling(symmetry=True)
    else:
        cmds.symmetricModelling(symmetry=False)

    # If it is a nurbs
    if 'nurbs' in cmds.nodeType(cmds.listRelatives(get_blend_shape_node(blend_shape=blend_shape),
                                                   shapes=True,
                                                   noIntermediate=True)[0]):
        for target_value in get_target_values(blend_shape=blend_shape, target=target):
            if target_value == 1:
                target_rebuild = cmds.sculptTarget(blend_shape,
                                                   edit=True,
                                                   regenerate=True,
                                                   target=get_target_index(blend_shape=blend_shape,
                                                                           target=target))[0]
                mirror_rebuild = cmds.sculptTarget(blend_shape,
                                                   edit=True,
                                                   regenerate=True,
                                                   target=get_target_index(blend_shape=blend_shape,
                                                                           target=mirror_target_name))[0]
            else:
                target_rebuild = cmds.sculptTarget(blend_shape,
                                                   edit=True,
                                                   regenerate=True,
                                                   target=get_target_index(blend_shape=blend_shape,
                                                                           target=target),
                                                   inbetweenWeight=target_value)[0]
                mirror_rebuild = cmds.sculptTarget(blend_shape,
                                                   edit=True,
                                                   regenerate=True,
                                                   target=get_target_index(blend_shape=blend_shape,
                                                                           target=mirror_target_name),
                                                   inbetweenWeight=target_value)[0]

            target_cv_list = cmds.ls('{}.cv[*]'.format(target_rebuild), flatten=True)

            source_cv_max = int(max(target_cv_list).split('.cv[')[-1].split(']')[0])
            for cv in target_cv_list:
                cv_index = int(cv.split('.cv[')[-1].split(']')[0])
                opposite_cv = list(range(0, source_cv_max + 1))[::-1][cv_index]

                cv_position = cmds.xform(cv, query=True, worldSpace=True, translation=True)

                cmds.xform(
                    cv.replace(target_rebuild, mirror_rebuild).replace('.cv[{}]'.format(cv_index),
                                                                       '.cv[{}]'.format(opposite_cv)),
                    worldSpace=True, translation=[cv_position[0] * -1, cv_position[1], cv_position[2]])

            cmds.delete(target_rebuild)
            cmds.delete(mirror_rebuild)


def copy_target_connection(source=None, target_list=None, *args):
    """
    copy blendShape target's connections
    :param source: str, blendShape.target
    :param target_list: list, [blendShape.target, ...]
    """
    if not source and not target_list:
        target_selection_list = get_targets_from_shape_editor(as_index=False)
        source = target_selection_list[0]
        target_list = target_selection_list[1:]

    source_input_connections = cmds.listConnections(source, destination=False, plugs=True)[0]
    for target in target_list:
        cmds.connectAttr(source_input_connections, target)


def order_shape_editor_blend_shapes(blend_shape_list):
    """
    Re-order the blend shapes in the shape editor
    :param blend_shape_list: list
    """
    # Shape editor index order
    blend_shape_index_order = cmds.getAttr('shapeEditorManager.blendShapeDirectory[0].childIndices')

    # Get blendShapes index in the shape editor
    blend_shape_dict = OrderedDict()
    for blend_shape in blend_shape_list[::-1]:
        check_blendshape(blend_shape)

        blend_shape_index = get_blend_shape_index(blend_shape=blend_shape)
        blend_shape_dict[blend_shape] = blend_shape_index

    # Re-order the shape editor index order
    for key, value in blend_shape_dict.items():
        blend_shape_index = int(blend_shape_dict[key])
        blend_shape_index_order.remove(blend_shape_index)
        blend_shape_index_order = [blend_shape_index] + blend_shape_index_order

    # Set the shape editor index order
    cmds.setAttr('shapeEditorManager.blendShapeDirectory[0].childIndices', blend_shape_index_order, type='Int32Array')
