# Imports
import logging
from collections import OrderedDict

# Maya imports
from maya import cmds, mel

# Project imports
from hiddenStrings.libs import side_lib, usage_lib, skin_lib, nurbs_lib

logging = logging.getLogger(__name__)


def check_blendshape(blend_shape):
    """
    Check if the blendshape node exists and if it is a blendShape

    Args:
        blend_shape (str): name of the blendshape
    """
    if not cmds.objExists(blend_shape):
        cmds.error(f'{blend_shape} does not exists in the scene')
    if cmds.objectType(blend_shape) != 'blendShape':
        cmds.error(f'{blend_shape} is not a blendShape')


def check_target(blend_shape, target):
    """
    Check if the blendshape target already exists

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target

    Returns:
        bool: True == target exists
    """
    check_blendshape(blend_shape=blend_shape)

    targets_list = get_blendshape_target_list(blend_shape=blend_shape)
    if targets_list and target in targets_list:
        return True
    else:
        return False


def check_in_between(blend_shape, target, value):
    """
    Check if the blendshape target in-between already exists

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target
        value (float): value of the in-between

    Returns:
        bool: True == in-between exists
    """
    target_index = get_target_index(blend_shape=blend_shape, target=target)
    target_data = cmds.listAttr(f'{blend_shape}.inputTarget[0].inputTargetGroup[{target_index}]', multi=True)

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
    Format the blendshape name giving a node

    Args:
        node (str): node name

    Returns:
        str: blendshape name formatted
    """
    if not node:
        logging.error('Invalid input for node')
        return
    if len(node.split('_')) != 3:
        return f'{node}_{usage_lib.blend_shape}'
    else:
        descriptor, side, usage = node.split('_')
        return f'{descriptor}{usage.capitalize()}_{side}_{usage_lib.blend_shape}'


def get_blend_shape(node):
    """
    Get blendShape attached to the node

    Args:
        node (str): name of the node

    Returns:
        str: blendshape node name
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

    Args:
        blend_shape (str): name of the blendshape

    Returns:
        str: node name
    """
    node_shape = cmds.blendShape(blend_shape, query=True, geometry=True)[0]
    node = cmds.listRelatives(node_shape, parent=True)[0]
    return node


def get_blend_shape_index(blend_shape):
    """
    Get the blendShape index

    Args:
        blend_shape (str): name of the blendshape

    Returns:
        str: blendshape index in the shapeEditor
    """
    return cmds.listConnections(f'{blend_shape}.midLayerParent', plugs=True)[0].split('[')[-1].split(']')[0]


def get_blendshape_target_list(blend_shape):
    """
    Get the blendshape targets names

    Args:
        blend_shape (str): name of the blendshape

    Returns:
        list: get the blendshape target list
    """
    target_list = cmds.aliasAttr(blend_shape, query=True)
    if target_list:
        return target_list[0::2]
    else:
        return None


def get_target_name(blend_shape, target_index):
    """
    Get the target's name

    Args:
        blend_shape (str): name of the blendshape
        target_index (float): number of the target

    Returns:
        str: target's name
    """
    target_list = cmds.aliasAttr(blend_shape, query=True)
    target_dict = dict()
    for target_name in target_list[1::2]:
        index = target_list.index(target_name)
        target_dict[target_name.split('[')[-1].split(']')[0]] = target_list[index - 1]

    return target_dict[str(target_index)]


def get_target_values(blend_shape, target):
    """
    Get the values of the in-betweens of a target (include the 1.0 value)

    Args:
        blend_shape (str): name of the blendshape
        target (str): target name

    Returns:
        list: values of the in-betweens, including the 1.0
    """
    check_blendshape(blend_shape=blend_shape)

    target_index = get_target_index(blend_shape=blend_shape, target=target)
    target_data = cmds.listAttr(f'{blend_shape}.inputTarget[0].inputTargetGroup[{target_index}]', multi=True)

    target_values_list = list()
    for target in target_data:
        if target.find("inputGeomTarget") != -1:
            target_value = target.split('.')[-2].split('[')[-1].split(']')[0]

            target_value = (int(target_value) - 5000) * 0.001
            target_values_list.append(target_value)

    return target_values_list


def get_target_index(blend_shape, target):
    """
    Get the index of a blendshape target

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target

    Returns:
        int: index of the target
    """
    check_blendshape(blend_shape=blend_shape)
   
    target_list = cmds.aliasAttr(blend_shape, query=True)

    if target_list and target in target_list:
        target_dict = dict()
        for target_name in target_list[0::2]:
            index = target_list.index(target)
            target_dict[target_name] = target_list[index + 1].split('[')[-1].split(']')[0]
        return int(target_dict[target])
    else:
        return None


def get_next_target_index(blend_shape):
    """
    Get the next target index of a blendshape

    Args:
        blend_shape (str): name of the blendshape

    Returns:
        int: next available target index of a blendshape
    """
    check_blendshape(blend_shape=blend_shape)

    target_list = cmds.aliasAttr(blend_shape, query=True)
    if target_list:
        target_index_list = list()
        for target_name in target_list[1::2]:
            target_index = target_name.split('[')[-1].split(']')[0]
            target_index_list.append(int(target_index))
        index = max(target_index_list) + 1

    else:
        index = 0

    return index


def get_in_between_value(blend_shape, target, in_between):
    """
    Get the in between value

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target
        in_between (str): in_between name

    Returns:
        float: in-between value
    """
    for value in get_target_values(blend_shape=blend_shape, target=target):
        in_between_name = cmds.getAttr('{}.inbetweenInfoGroup[{}].inbetweenInfo[5{}].inbetweenTargetName'.format(
                                                                            blend_shape,
                                                                            get_target_index(blend_shape, target),
                                                                            str(value).split('.')[-1]))
        if in_between_name == in_between:
            return value


def get_blend_shapes_from_shape_editor():
    """
    Get blendShapes from the shape editor

    Returns:
        list: [blendShape1, blendShape2, ...]
    """
    return mel.eval('getShapeEditorTreeviewSelection(1)')


def get_targets_from_shape_editor(as_index=True):
    """
    Get targets from the shape editor

    Args:
        as_index (bool, optional): if we need the targets as index. Defaults to True.

    Returns:
        list: as_index == [blendShape1.0, blendShape1.1, ...] else [blendShape1.target, ...]
    """
    selection_list = mel.eval('getShapeEditorTreeviewSelection(4)')
    if not as_index:
        selection_list = ['{}.{}'.format(x.split('.')[0],
                                         get_target_name(blend_shape=x.split('.')[0],
                                                         target_index=x.split('.')[1])) for x in selection_list]

    return selection_list


def get_in_betweens_from_shape_editor(as_index=True):
    """
    Get in-between targets from the shape editor

    Args:
        as_index (bool, optional): if we need the in-between as index. Defaults to True.

    Returns:
        list: [blendShape1.0.5500, blendShape1.0.5300, ...]
    """
    selection_list = mel.eval("getShapeEditorTreeviewSelection(16)")
    if not as_index:
        selection_list = ['{}.{}.{}'.format(
                                x.split('.')[0], 
                                get_target_name(blend_shape=x.split('.')[0],
                                                target_index=x.split('.')[1]),
                                cmds.getAttr('{}.inbetweenInfoGroup[{}].inbetweenInfo[{}].inbetweenTargetName'.format(
                                                                                                    x.split('.')[0],
                                                                                                    x.split('.')[1],
                                                                                                    x.split('.')[2])))
                          for x in selection_list]

    return selection_list


def get_blend_shape_data(blend_shape):
    """
    Get blendshape data, including target in-between values and deltas

    Args:
        blend_shape (str): name of the blendshape

    Returns:
        dict: blendshape data
    """
    check_blendshape(blend_shape=blend_shape)

    blend_shape_data = OrderedDict()

    blend_shape_data['node'] = get_blend_shape_node(blend_shape)
    blend_shape_data['blendShape'] = blend_shape
    blend_shape_data['targets'] = dict()

    targets_order_list = cmds.getAttr(f'{blend_shape}.targetDirectory[0].childIndices')
    for target_order in targets_order_list:
        target = get_target_name(blend_shape=blend_shape, target_index=target_order)

        blend_shape_data['targets'][target] = get_target_data(blend_shape=blend_shape, target=target)

    return blend_shape_data


def get_target_data(blend_shape, target):
    """
    Get target data, including in-betweens values and deltas

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target

    Returns:
        dict: target data
    """
    target_dict = dict()

    target_dict['envelope'] = round(cmds.getAttr(f'{blend_shape}.{target}'), 3)

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
    Set blendShape data including targets, in-betweens values and deltas

    Args:
        blend_shape (str): name of the blendshape
        blend_shape_data (dict): blendshape data dict from get_blend_shape_data
    """
    for target in blend_shape_data['targets']:
        set_target_data(blend_shape=blend_shape, target=target, target_data=blend_shape_data['targets'][target])


def set_target_data(blend_shape, target, target_data):
    """
    Set target data including in-betweens values and deltas

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target
        target_data (dict): blendshape target data dict from the get_target_data
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
                           in_between_target=f'{target}_{pretty_target_value}',
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
                         f'{target}_{pretty_target_value}',
                         type='string')

        if cmds.getAttr(f'{blend_shape}.{target}', settable=True):
            cmds.setAttr(f'{blend_shape}.{target}', target_data['envelope'])


def rename_blend_shape(blend_shape):
    """
    Rename a blendshape with the get_blendshape_name value

    Args:
        blend_shape (str): name of the blendshape

    Returns:
        str: new name of the blendshape
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


def rename_target(blend_shape, target, new_name):
    """
    Rename a blendshape target

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target
        new_name (str): new name for the target

    Returns:
        str: new target name
    """
    if new_name != target:
        cmds.aliasAttr(new_name, f'{blend_shape}.{target}')

    return new_name


def rename_in_between(blend_shape, target, in_between, new_name):
    """
    Rename an in-between target

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target
        in_between (str): name of the in-between
        new_name (str): new name for the in-betwee ntarget

    Returns:
        str: new in-between target
    """
    target_index = get_target_index(blend_shape, target)
    in_between_value = str(get_in_between_value(blend_shape=blend_shape, target=target, in_between=in_between))
    cmds.setAttr('{}.inbetweenInfoGroup[{}].inbetweenInfo[5{}].inbetweenTargetName'.format(
                                                                                blend_shape,
                                                                                target_index,
                                                                                in_between_value.split('.')[-1]), 
                new_name,
                type='string')

    return new_name


def create_blend_shape(node, target_list=None):
    """
    Create a blendshape

    Args:
        node (str): name of the node
        target_list (list, optional): list of targets, None == blendshape without targets. Defaults to None.

    Returns:
        str: name of the blendshape
    """
    blend_shape = cmds.blendShape(node, topologyCheck=False, name=get_blend_shape_name(node))[0]
    if target_list:
        for target in target_list:
            add_target(blend_shape=blend_shape, target=target)

    return blend_shape


def add_target(blend_shape, target):
    """
    Add target to an existing blendShape

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the new target

    Returns:
        str: target name
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

        cmds.blendShape(blend_shape, edit=True, resetTargetDelta=(0, index))

    return get_target_name(blend_shape=blend_shape, target_index=index)


def add_in_between(blend_shape, existing_target, in_between_target, value):
    """
    Add an in-between to a target

    Args:
        blend_shape (str): name of the blendshape
        existing_target (str): name of the target
        in_between_target (str): name of the in-between target
        value (float): from 0 to 1
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
    Remove a target from its blendshape

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target
    """
    check_blendshape(blend_shape=blend_shape)

    target_index = get_target_index(blend_shape=blend_shape, target=target)
    mel.eval(f'blendShapeDeleteTargetGroup {blend_shape} {target_index}')


def remove_in_between(blend_shape, target, value):
    """
    Remove an in-between from its target

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target
        value (float): from 0 to 1. Value of the in-between
    """
    check_blendshape(blend_shape=blend_shape)

    index = get_target_index(blend_shape=blend_shape, target=target)

    if check_in_between(blend_shape=blend_shape, target=target, value=value):
        value = float(value)
        value = value * 1000 + 5000

        mel.eval(f'blendShapeDeleteInBetweenTarget {blend_shape} {index} {value}')
    else:
        cmds.error(f'the in-between at {value} does not exists in {blend_shape}.{target}')


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
    Mirror blendShape target 

    Args:
        blend_shape (str): name of the blendshape
        target (str): name of the target
    """
    # Get mirror target name
    if len(target.split('_')) == 3:
        descriptor, side, usage = target.split('_')
    else:
        descriptor = target
        side = side_lib.left
        usage = usage_lib.corrective
    target_mirror_name = f'{descriptor}_{side_lib.get_opposite_side(side)}_{usage}'

    # Get target data
    target_data = get_target_data(blend_shape=blend_shape, target=target)

    # Set target data in the mirror target
    set_target_data(blend_shape=blend_shape, target=target_mirror_name, target_data=target_data)

    # Mirror target
    get_symmetry = cmds.symmetricModelling(query=True, symmetry=True)

    target_index = get_target_index(blend_shape, target_mirror_name)

    cmds.blendShape(blend_shape, edit=True, symmetryAxis='x', symmetrySpace=1, flipTarget=[0, target_index])

    if get_symmetry:
        cmds.symmetricModelling(symmetry=True)
    else:
        cmds.symmetricModelling(symmetry=False)

    # If it is not a geometry
    node_type = cmds.nodeType(cmds.listRelatives(get_blend_shape_node(blend_shape=blend_shape),
                                                 shapes=True,
                                                 noIntermediate=True)[0])

    if 'mesh' not in node_type:
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
                                                                           target=target_mirror_name))[0]
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
                                                                           target=target_mirror_name),
                                                   inbetweenWeight=target_value)[0]

            # If it is a curve
            if 'nurbsCurve' in node_type:
                component_type = 'cv'

                target_cv_list = cmds.ls(f'{target_rebuild}.{component_type}[*]', flatten=True)

                target_cv_indices = [int(cv.split('[')[1].split(']')[0]) for cv in target_cv_list]

                source_cv_max = int(max(target_cv_indices))

                for cv in target_cv_list:
                    cv_position = cmds.xform(cv, query=True, objectSpace=True, translation=True)

                    cv_index = int(cv.split('[')[1].split(']')[0])

                    opposite_cv = list(range(0, source_cv_max + 1))[::-1][cv_index]

                    cmds.xform(cv.replace(
                            target_rebuild, mirror_rebuild).replace(f'.{component_type}[{cv_index}]',
                                                                    f'.{component_type}[{opposite_cv}]'),
                        objectSpace=True, translation=[cv_position[0] * -1, cv_position[1], cv_position[2]])

            # If it is a nurbs
            if 'nurbsSurface' in node_type:
                component_type = 'cv'

                target_cv_list = cmds.ls(f'{target_rebuild}.{component_type}[*]', flatten=True)
                print(max(target_cv_list), target_cv_list)
                param_x = nurbs_lib.get_param_along_x(nurbs=target_rebuild)

                target_cv_u_indices = [int(cv.split('[')[1].split(']')[0]) for cv in target_cv_list]
                target_cv_v_indices = [int(cv.split('[')[2].split(']')[0]) for cv in target_cv_list]

                source_u_max = int(max(target_cv_u_indices))
                source_v_max = int(max(target_cv_v_indices))

                for cv in target_cv_list:
                    cv_position = cmds.xform(cv, query=True, objectSpace=True, translation=True)

                    u_index = int(cv.split('[')[1].split(']')[0])
                    v_index = int(cv.split('[')[2].split(']')[0])
                    
                    opposite_u = list(range(0, source_u_max + 1))[::-1][u_index]
                    opposite_v = list(range(0, source_v_max + 1))[::-1][v_index]

                    if param_x == 'U':
                        cmds.xform(
                            cv.replace(
                                target_rebuild, mirror_rebuild).replace('.{}[{}][{}]'.format(component_type,
                                                                                             u_index, v_index),
                                                                        '.{}[{}][{}]'.format(component_type,
                                                                                             opposite_u, v_index)),
                            objectSpace=True, translation=[cv_position[0] * -1, cv_position[1], cv_position[2]])
                    else:
                        cmds.xform(
                            cv.replace(
                                target_rebuild, mirror_rebuild).replace('.{}[{}][{}]'.format(component_type,
                                                                                             u_index, v_index),
                                                                        '.{}[{}][{}]'.format(component_type,
                                                                                             u_index, opposite_v)),
                            objectSpace=True, translation=[cv_position[0] * -1, cv_position[1], cv_position[2]])

            # If it is a lattice
            if 'lattice' in node_type:
                component_type = 'pt'

                target_pt_list = cmds.ls(f'{target_rebuild}.{component_type}[*]', flatten=True)

                target_pt_x_indices = [int(pt.split('[')[1].split(']')[0]) for pt in target_pt_list]

                source_x_max = int(max(target_pt_x_indices))

                for cv in target_pt_list:
                    cv_position = cmds.xform(cv, query=True, objectSpace=True, translation=True)

                    x_index = int(cv.split('['.format(component_type))[1].split(']')[0])
                    y_index = int(cv.split('['.format(component_type))[2].split(']')[0])
                    z_index = int(cv.split('['.format(component_type))[3].split(']')[0])

                    opposite_x = list(range(0, source_x_max + 1))[::-1][x_index]
                    cmds.xform(cv.replace(
                            target_rebuild, mirror_rebuild).replace('.{}[{}][{}][{}]'.format(component_type,
                                                                                             x_index, 
                                                                                             y_index, 
                                                                                             z_index),
                                                                    '.{}[{}][{}][{}]'.format(component_type,
                                                                                             opposite_x, 
                                                                                             y_index, 
                                                                                             z_index)),
                        objectSpace=True, translation=[cv_position[0] * -1, cv_position[1], cv_position[2]])

            cmds.delete(target_rebuild)
            cmds.delete(mirror_rebuild)
    
    logging.info(f'{target} has been transfered and flipped to --> {target_mirror_name}')


def copy_target_connection(source=None, destination_list=None, *args):
    """
    Copy blendShape target's connections

    Args:
        source (str, optional): name of the source target. None == selection 0. Defaults to None.
        destination_list (str, optional): name of the destination target. None == selection 1. Defaults to None.
    """
    if not source and not destination_list:
        target_selection_list = get_targets_from_shape_editor(as_index=False)
        source = target_selection_list[0]
        destination_list = target_selection_list[1:]

    source_input_connections = cmds.listConnections(source, destination=False, plugs=True)
    if source_input_connections:
        source_input_connections = source_input_connections[0]
        for target in destination_list:
            cmds.connectAttr(source_input_connections, target)


def copy_blendshape_connections(source=None, destination_list=None, *args):
    """_summary_
    Copy blendShape targets' connections

    Args:
        source (str, optional): name of the source blendshape. None == selection 0. Defaults to None.
        destination_list (list, optional): [blendShape1, ...]. None == selection 1, 2, 3.... Defaults to None.
    """
    if not source and not destination_list:
        blendshape_list = get_blend_shapes_from_shape_editor()

        if len(blendshape_list) > 0:
            source = blendshape_list[0]
            destination_list = blendshape_list[1:]
        else:
            source = cmds.ls(selection=True)[0]
            destination_list = cmds.ls(selection=True)[1:]

    # Get the targets' names
    source_target_list = get_blendshape_target_list(blend_shape=source)

    # Check if the destination have the same target and connect it
    for destination in destination_list:
        for target in source_target_list:
            if check_target(blend_shape=destination, target=target):
                copy_target_connection(source=f'{source}.{target}',
                                       destination_list=[f'{destination}.{target}'])
            else:
                logging.info(f'{destination}.{target} does not exists.')


def transfer_blend_shape(source=None, destination=None, *args):
    """
    Transfer blendshape from source to destination

    Args:
        source (str, optional): name of the source blendshape. None == selection 0. Defaults to None.
        destination (str, optional): name of the destination blendshape. None == selection 1. Defaults to None.
    """
    if not source and not destination: # If the inputs are None
        blendshape_list = get_blend_shapes_from_shape_editor()

        if len(blendshape_list) >= 2: # If there is blendShapes selected in the shapeEditor
            source = blendshape_list[0]
            destination = blendshape_list[1]
        else: # if the inputs are None and we dont have blendShapes selected in the shapeEditor then
            selection_list = cmds.ls(selection=True)
            if selection_list:
                source = selection_list[0]
                destination = selection_list[1]

                if cmds.objectType(source, isType='transform'):
                    source = get_blend_shape(source)
                if cmds.objectType(destination, isType='transform'):
                    if get_blend_shape(destination):
                        destination = get_blend_shape(destination)
                    else:
                        destination = create_blend_shape(node=destination)
            else:
                logging.error('select two geometries (source with blendShape and target)' +
                              'or select blendShapes in the shapeEditor')
                return

    # Create the source base geometry
    source_base = cmds.rename(cmds.listRelatives(cmds.createNode('mesh'), parent=True)[0], 
                              f'{source}Base')
    source_base_shape = cmds.listRelatives(source_base, shapes=True, noIntermediate=True)[0]

    cmds.connectAttr(f'{source}.originalGeometry[0]', f'{source_base_shape}.inMesh')

    # Create the destination base geometry
    destination_base = cmds.rename(cmds.listRelatives(cmds.createNode('mesh'), parent=True)[0], 
                                   f'{destination}Base')
    destination_base_shape = cmds.listRelatives(destination_base, shapes=True, noIntermediate=True)[0]

    cmds.connectAttr(f'{destination}.originalGeometry[0]', f'{destination_base_shape}.inMesh')

    # Wrap
    cmds.select(destination_base)
    proximity_wrap = cmds.deformer(type='proximityWrap')[0]
    cmds.setAttr(f'{proximity_wrap}.wrapMode', 0)

    # Get source target list
    source_target_list = get_blendshape_target_list(blend_shape=source)

    # Delete old targets
    for target in source_target_list:
        if check_target(blend_shape=destination, target=target):
            remove_target(blend_shape=destination, target=target)

    # Transfer each target
    for target in source_target_list:
        target_values = get_target_values(blend_shape=source, target=target)
        for value in target_values[::-1]:
            if value == 1.0:
                source_rebuild = cmds.sculptTarget(source, edit=True, regenerate=True,
                                                   target=get_target_index(blend_shape=source, target=target))[0]
            else:
                source_rebuild = cmds.sculptTarget(source, edit=True, regenerate=True,
                                                   target=get_target_index(blend_shape=source, target=target),
                                                   inbetweenWeight=value)[0]

            temporal_blend_shape = create_blend_shape(node=source_base, target_list=[source_rebuild])
            cmds.setAttr('{}.{}'.format(temporal_blend_shape, get_target_name(blend_shape=temporal_blend_shape,
                                                                              target_index=0)), 1)

            # Wrap driver connections (now that we have the shapeOrig)
            if not cmds.isConnected(f'{source_base_shape}Orig.outMesh',
                                    f'{proximity_wrap}.drivers[0].driverBindGeometry'):
                cmds.connectAttr(f'{source_base_shape}Orig.outMesh',
                                 f'{proximity_wrap}.drivers[0].driverBindGeometry')
                cmds.connectAttr(f'{source_base_shape}.outMesh',
                                 f'{proximity_wrap}.drivers[0].driverGeometry')

            delta = cmds.duplicate(destination_base)[0]

            if value == 1.0:
                new_target = add_target(blend_shape=destination, target=delta)
                rename_target(blend_shape=destination, target=new_target, new_name=target)
                copy_target_connection(source=f'{source}.{target}',
                                       destination_list=[f'{destination}.{target}'])
            else:
                add_in_between(blend_shape=destination, existing_target=target, in_between_target=delta, value=value)

            cmds.delete(source_rebuild, temporal_blend_shape, delta)

    cmds.delete(source_base, destination_base)


def order_shape_editor_blend_shapes(blend_shape_list):
    """
    Re-order the blend shapes in the shape editor

    Args:
        blend_shape_list (list): new blendshape order
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


def automatic_corrective(geometry_name='test_c_geo',
                         control_name='test_c_ctr',
                         attr_name='rotateZ',
                         attr_value=-90,
                         create_sdk=True):
    """
    Creates a blendshape target with a delta mush

    Args:
        geometry_name (str, optional): name of the geometry. Defaults to 'test_c_geo'.
        control_name (str, optional): name of the control. Defaults to 'test_c_ctr'.
        attr_name (str, optional): name of the attribute. Defaults to 'rotateZ'.
        attr_value (int, optional): value of the attribute. Defaults to -90.
        create_sdk (bool, optional): Create set driven key curve. Defaults to True.
    """
    if len(control_name.split('_')) == 3:
        control_descriptor, control_side = control_name.split('_')[:2]
    else:
        control_descriptor = control_name
        control_side = side_lib.center

    default_attr_value = cmds.getAttr(f'{control_name}.{attr_name}')

    # Get blendshape
    blend_shape = get_blend_shape(node=geometry_name)

    # Create target
    attr_value_formatted = str(attr_value).replace('-', 'M').replace('.', 'd')
    target_name = '{}{}{}{}_{}_{}'.format(control_descriptor,
                                          attr_name[0].upper(),
                                          attr_name[-1].lower(),
                                          attr_value_formatted,
                                          control_side,
                                          usage_lib.corrective)

    if check_target(blend_shape=blend_shape, target=target_name):
        logging.error(f'{blend_shape}.{target_name} already exists, delete it before using this tool')
        return

    target = add_target(blend_shape=blend_shape, target=target_name)
    target = rename_target(blend_shape=blend_shape, target=target, new_name=target_name)

    # Set skinCluster to dualQuaternion
    cmds.refresh()
    skin_name = skin_lib.get_skin_cluster_index(node=geometry_name)
    if not skin_name:
        cmds.error('The geometry given has not a skinCluster')

    # Create delta Mush
    cmds.refresh()
    delta_mush_name = cmds.deltaMush(geometry_name, smoothingIterations=10, smoothingStep=0.5, envelope=1)[0]
    cmds.setAttr(f'{delta_mush_name}.distanceWeight', 1)
    cmds.setAttr(f'{delta_mush_name}.inwardConstraint', 1)

    skin_method_default_value = cmds.getAttr(f'{skin_name}.skinningMethod')
    cmds.setAttr(f'{skin_name}.skinningMethod', 1)

    # Set pose
    cmds.refresh()
    cmds.setAttr(f'{control_name}.{attr_name}', attr_value)

    # Extract delta
    cmds.refresh()
    delta = cmds.duplicate(geometry_name, name=target)[0]

    # Set skinCluster to its default
    cmds.refresh()
    cmds.setAttr(f'{skin_name}.skinningMethod', skin_method_default_value)

    # Delete deltaMush
    cmds.delete(delta_mush_name)

    # Add target
    cmds.refresh()
    target_index = get_target_index(blend_shape=blend_shape, target=target)

    cmds.setAttr(f'{blend_shape}.{target}', 1)

    cmds.sculptTarget(blend_shape, edit=True, target=target_index)
    cmds.transferShape(source=delta, target=geometry_name, worldSpace=True)
    cmds.sculptTarget(blend_shape, edit=True, target=target_index)

    cmds.delete(delta)

    cmds.setAttr(f'{control_name}.{attr_name}', default_attr_value)

    # Anim curve creation
    if create_sdk:
        sdk_name = '{}{}{}{}_{}_{}'.format(control_descriptor, attr_name[0].upper(), attr_name[-1].upper(),
                                           attr_value_formatted, control_side, usage_lib.animation_curve)
        sdk_name = cmds.createNode('animCurveUU', name=sdk_name)
        cmds.setKeyframe(sdk_name, float=default_attr_value, value=0, inTangentType='linear', outTangentType='linear')
        cmds.setKeyframe(sdk_name, float=attr_value, value=1, inTangentType='linear', outTangentType='linear')

        # Connections
        cmds.connectAttr(f'{control_name}.{attr_name}', f'{sdk_name}.input')
        cmds.connectAttr(f'{sdk_name}.output', f'{blend_shape}.{target}')

    else:
        cmds.setAttr(f'{blend_shape}.{target}', 0)
