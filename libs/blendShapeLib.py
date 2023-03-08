# Imports
import os
from collections import OrderedDict
# Maya imports
from maya import mel, cmds

# Project imports
from hiddenStrings.libs import usageLib, jsonLib


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
        return '{}_{}'.format(node, usageLib.blend_shape)
    else:
        descriptor, side, usage = node.split('_')
        return '{}{}_{}_{}'.format(descriptor, usage.capitalize(),
                                   side,
                                   usageLib.blend_shape)


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


def get_target_name(blend_shape, target_index):
    """
    Get the target's name
    :param blend_shape: str
    :param target_index: int
    :return: target name
    """
    return cmds.listAttr('{}.weight[{}]'.format(blend_shape, target_index))[0]


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


def get_blend_shape_data(blend_shape):
    """
    Get blendshape data, including target in betweens values and deltas
    :param blend_shape: str
    """
    check_blendshape(blend_shape=blend_shape)

    blend_shape_data = OrderedDict()

    blend_shape_data['node'] = get_blend_shape_node(blend_shape)
    blend_shape_data['blendShape'] = blend_shape
    blend_shape_data['targets'] = dict()

    # targets_list = cmds.listAttr('{}.weight'.format(blend_shape), multi=True)
    targets_order_list = cmds.getAttr('{}.targetDirectory[0].childIndices'.format(blend_shape))
    for target_order in targets_order_list:
        target = get_target_name(blend_shape=blend_shape, target_index=target_order)
        print(target)
        blend_shape_data['targets'][target] = dict()
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

            blend_shape_data['targets'][target][target_value] = target_data

    return blend_shape_data


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


def transfer_blend_shape(source, target):
    """
    Transfer the blendshape targets with cvWrap
    :param source: str
    :param target: str
    """
    pass


def export_blend_shape(node, path):
    """
    Export blendShape of the node given
    :param node: str
    :param path: str
    """
    if not cmds.objExists(node):
        cmds.error('{} does not exists in the scene'.format(node))
    blend_shape_name = get_blend_shape(node)

    check_blendshape(blend_shape=blend_shape_name)
    blend_shape_data = get_blend_shape_data(blend_shape_name)

    jsonLib.export_data_to_json(data=blend_shape_data, file_name=blend_shape_name, file_path=path, relative_path=False,
                                compact=True)

    print(end='\n')
    print(end='{} has been exported'.format(path))


def export_blend_shapes(node_list, path):
    """
    Export blendShapes of the nodes given
    :param node_list: list
    :param path: str
    """
    for node in node_list:
        export_blend_shape(node=node, path=path)


def import_blend_shape(node, path):
    """
    Import blendShape from path
    :param node: str
    :param path: str
    """
    file_name = os.path.basename(path).split('.json')[0]
    path = os.path.dirname(path)

    blend_shape = get_blend_shape(node=node)
    if blend_shape:
        blend_shape = rename_blend_shape(blend_shape=blend_shape)
    else:
        blend_shape = create_blend_shape(node=node)

    blend_shape_data = jsonLib.import_data_from_json(file_name=file_name, file_path=path, relative_path=False)
    for target in blend_shape_data['targets']:
        if not check_target(blend_shape=blend_shape, target=target):
            add_target(blend_shape=blend_shape, target=target)

        target_index = get_target_index(blend_shape=blend_shape, target=target)
        for target_value in blend_shape_data['targets'][target]:
            points_target = blend_shape_data['targets'][target][target_value]['inputPointsTarget']
            components_target = blend_shape_data['targets'][target][target_value]['inputComponentsTarget']
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
    print(end='\n')
    print(end=r'{}\{}.json has been imported'.format(path, file_name))


def import_blend_shapes(path):
    """
    Import all json blendShapes from folder
    :param path: string
    """
    file_list = [x for x in os.listdir(path) if x.endswith('.json')]
    for blend_shape_file in file_list:
        # Get json file node
        blend_shape_data = jsonLib.import_data_from_json(file_name=blend_shape_file.split('.')[0],
                                                         file_path=path,
                                                         relative_path=False)

        import_blend_shape(node=blend_shape_data['node'], path=r'{}\{}'.format(path, blend_shape_file))
    pass


def edit_target_or_in_between(*args):
    """
    Set on edit a target or an in-between target even when there is a direct connection
    """
    inbetween_shape_editor_values = mel.eval('getShapeEditorTreeviewSelection(16)')
    if inbetween_shape_editor_values:
        blendshape_node, target_index, inbetween_index = inbetween_shape_editor_values[0].split('.')

        inbetween_value = (float(inbetween_index) / 1000.0) - 5

        cmds.sculptTarget(blendshape_node, edit=True, target=int(target_index), inbetweenWeight=inbetween_value)

    else:
        target_shape_editor_values = mel.eval('getShapeEditorTreeviewSelection(24)')
        if target_shape_editor_values:
            blendshape_node, target_index = target_shape_editor_values[0].split('.')
            cmds.sculptTarget(blendshape_node, edit=True, target=int(target_index))


# bs_list = cmds.getAttr('shapeEditorManager.blendShapeDirectory[0].childIndices')
# new_bs_order = [2, 1]
#
# for index in new_bs_order:
#     bs_list.remove(index)
#
# new_bs_order = new_bs_order + bs_list
#
# cmds.setAttr('shapeEditorManager.blendShapeDirectory[0].childIndices', new_bs_order, type='Int32Array')


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

        blend_shape_index = cmds.listConnections('{}.midLayerParent'.format(blend_shape),
                                                 plugs=True)[0].split('[')[-1].split(']')[0]
        blend_shape_dict[blend_shape] = blend_shape_index

    # Re-order the shape editor index order
    for key, value in blend_shape_dict.items():
        blend_shape_index = int(blend_shape_dict[key])
        blend_shape_index_order.remove(blend_shape_index)
        blend_shape_index_order = [blend_shape_index] + blend_shape_index_order

    # Set the shape editor index order
    cmds.setAttr('shapeEditorManager.blendShapeDirectory[0].childIndices', blend_shape_index_order, type='Int32Array')

