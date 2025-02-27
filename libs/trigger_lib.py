# imports

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings import module_utils
from hiddenStrings.libs import (import_export_lib, attribute_lib, connection_lib, bifrost_lib, vector_lib,
                                side_lib, usage_lib)


def create_bary_trigger(descriptor='bary', side=side_lib.center,
                        parent_node=None,
                        driver_node=None):
    """
    Create a bary trigger with bifrost

    Args:
        descriptor (str): descriptor. Defaults to 'bary'.
        side (str): side
        parent_node (str): parent node. Defaults to None.
        driver_node (str): driver node. Defaults to None.
    """
    bary_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(descriptor,
                                                                     usage_lib.get_usage_capitalize(usage_lib.trigger),
                                                                     side,
                                                                     usage_lib.group))

    # Create Bary geometry
    bary_geo = import_export_lib.import_obj(
        path=r'{}/libs/geo_shapes/bary.obj'.format(module_utils.hidden_strings_path))[0]
    bary_geo = cmds.rename(bary_geo, f'{descriptor}_{side}_{usage_lib.geometry}')
    bary_geo_shape = cmds.listRelatives(bary_geo, allDescendents=True, shapes=True, noIntermediate=True)[0]

    # Create bary node (bifrost graph)
    compound_namespace = 'rigging'
    compound_name = 'barycentricPoseReader'

    source_file = r'{}/bifrost/{}.json'.format(module_utils.hidden_strings_path, compound_name)

    bifrost_lib.copy_bifrost_compound(source_file=source_file, destination_dir=bifrost_lib.bifrost_path, force=True)

    bary_shape = bifrost_lib.import_compound(compound_namespace=compound_namespace, compound_name=compound_name)
    bary_trigger = cmds.rename(cmds.listRelatives(bary_shape, parent=True)[0],
                               f'{descriptor}_{side}_{usage_lib.trigger}')
    bary_shape = cmds.listRelatives(bary_trigger, allDescendents=True, shapes=True, noIntermediate=True)[0]

    cmds.parent(bary_geo, bary_trigger)
    cmds.parent(bary_geo_shape, bary_trigger, relative=True, shape=True)
    cmds.delete(bary_geo)

    cmds.parent(bary_trigger, bary_grp)

    # Create driver
    driver_shape = cmds.createNode('locator', name=f'{descriptor}_{side}_{usage_lib.driver}Shape')
    driver = cmds.rename(cmds.listRelatives(driver_shape, parent=True)[0],
                         f'{descriptor}_{side}_{usage_lib.driver}')
    cmds.parent(driver, bary_grp)

    for axis in 'XYZ':
        cmds.setAttr(f'{driver_shape}.localScale{axis}', 0.25)
    # Connect driver and shape to the bary node
    cmds.connectAttr(f'{bary_geo_shape}.worldMesh', f'{bary_shape}.mesh')
    cmds.connectAttr(f'{driver}.worldMatrix', f'{bary_shape}.driverMatrix')

    # Create outputs
    vertex_length = len(cmds.ls(f'{bary_geo_shape}.vtx[*]', flatten=True))

    driver_ah = attribute_lib.Helper(driver)

    driver_ah.lock_and_hide_attributes(attributes_list=['scaleX', 'scaleY', 'scaleZ',
                                                        'visibility'])
    driver_ah.add_separator_attribute(separator_name='Attributes')

    driver_ah.add_enum_attribute(attribute_name='driverAxis', states='X:-X:Y:-Y:Z:-Z', keyable=False)
    cmds.connectAttr(f'{driver}.driverAxis', f'{bary_shape}.driverAxis')
    driver_ah.add_separator_attribute(separator_name='Weights')
    weight_attribute = 'weight'
    for index in range(vertex_length):
        driver_ah.add_float_attribute(attribute_name=f'{weight_attribute}{str(index)}')
        cmds.connectAttr(f'{bary_shape}.baryWeight[{str(index)}]',
                         f'{driver}.{weight_attribute}{str(index)}')

    if parent_node and driver_node:
        cmds.xform(bary_trigger, worldSpace=True,
                   matrix=cmds.xform(driver_node, query=True, worldSpace=True, matrix=True))

        connection_lib.connect_offset_parent_matrix(driver=parent_node, driven=bary_trigger)

        cmds.xform(driver, worldSpace=True,
                   matrix=cmds.xform(bary_trigger, query=True, worldSpace=True, matrix=True))

    if parent_node and driver_node:
        connection_lib.connect_offset_parent_matrix(driver=driver_node, driven=driver)


def create_angle_trigger(parent_node, driver_node,
                         forbidden_word='01',
                         structural_parent='triggers_c_grp'):
    """
    Create an angle trigger system

    Args:
    parent_node (str): parent node
    driver_node (str): driver node
    forbidden_word (str): forbidden words to avoid in the name. Defaults to '01'.
    structural_parent (str): structutal parent node. Defaults to 'triggers_c_grp'.
    """
    # Splitting names for renaming all the nodes
    if len(parent_node.split('_')) == 3:
        parent_descriptor, parent_side, parent_usage = parent_node.split('_')
    else:
        parent_descriptor = parent_node
        parent_side = side_lib.center
        parent_usage = ''

    if len(driver_node.split('_')) == 3:
        descriptor, side, usage = driver_node.split('_')
    else:
        descriptor = driver_node
        side = side_lib.center

    if forbidden_word:
        descriptor = ''.join(descriptor.split(forbidden_word))

    # Create structural parent if it does not exist
    if not cmds.objExists(structural_parent):
        cmds.createNode('transform', name=structural_parent)

    # Create Angle reader group
    angle_reader_group = cmds.createNode('transform', name=f'{descriptor}AngleReader_{side}_grp',
                                         parent=structural_parent)

    cmds.xform(angle_reader_group, worldSpace=True,
               matrix=cmds.xform(driver_node, query=True, worldSpace=True, matrix=True))

    connection_lib.connect_offset_parent_matrix(driver=parent_node, driven=angle_reader_group)

    # Create the reader
    ref_reader = cmds.createNode('transform', name=f'{descriptor}Reader_{side}_{usage_lib.reference}',
                                 parent=angle_reader_group)
    ref_reader_static = cmds.createNode('transform',
                                        name=f'{descriptor}ReaderStatic_{side}_{usage_lib.reference}',
                                        parent=angle_reader_group)

    # Give the position to the reader
    reader_mult_mat = cmds.createNode('multMatrix',
                                      name=f'{driver_node}ReaderRef_{side}_{usage_lib.mult_matrix}')

    cmds.connectAttr(f'{driver_node}.worldMatrix', f'{reader_mult_mat}.matrixIn[0]')
    cmds.connectAttr(f'{parent_node}.worldInverseMatrix', f'{reader_mult_mat}.matrixIn[1]')
    cmds.setAttr(f'{reader_mult_mat}.matrixIn[2]',
                 cmds.getAttr(f'{parent_node}.worldMatrix'), type='matrix')
    cmds.setAttr(f'{reader_mult_mat}.matrixIn[3]',
                 cmds.getAttr(f'{driver_node}.worldInverseMatrix'), type='matrix')

    cmds.connectAttr(f'{reader_mult_mat}.matrixSum', f'{ref_reader}.offsetParentMatrix')
    cmds.setAttr(f'{ref_reader}.translateX', 1)
    cmds.setAttr(f'{ref_reader_static}.translateX', 1)

    cmds.setAttr(f'{ref_reader}.displayHandle', 1)
    cmds.setAttr(f'{ref_reader_static}.displayHandle', 1)

    # Create a vector for the reader
    vector_reader_pma = vector_lib.create_pma_vector_from_a_to_b(a=angle_reader_group, b=ref_reader)
    vector_reader_static_pma = vector_lib.create_pma_vector_from_a_to_b(a=angle_reader_group, b=ref_reader_static)

    # Create attribute helper and separator
    reader_ah = attribute_lib.Helper(ref_reader)
    reader_ah.add_separator_attribute(separator_name='Outputs')

    for num in ['01', '02', '03', '04']:
        # Create a reader in each direction
        ref_transform = cmds.createNode('transform',
                                        name=f'{descriptor}Reader{num}_{side}_{usage_lib.reference}',
                                        parent=angle_reader_group)

        # Give the position to each transform
        axis = 'Y' if num == '01' or num == '03' else 'Z'
        value = 1 if num == '01' or num == '02' else -1

        cmds.setAttr(f'{ref_transform}.translate{axis}', value)
        cmds.setAttr(f'{ref_transform}.displayHandle', 1)

        # Create a vector for each direction
        vector_pma = vector_lib.create_pma_vector_from_a_to_b(a=angle_reader_group, b=ref_transform)

        # Create an angle between for each direction
        angle_between = vector_lib.create_angle_between_two_pma_nodes(vector_pma, vector_reader_pma)
        angle_between_static = vector_lib.create_angle_between_two_pma_nodes(vector_pma, vector_reader_static_pma)

        # Remap values to normalize the outputs
        remap_value = cmds.createNode('remapValue',
                                      name=f'{descriptor}Reader{num}_{side}_{usage_lib.remap_value}')

        cmds.connectAttr(angle_between, f'{remap_value}.inputValue')
        cmds.connectAttr(angle_between_static, f'{remap_value}.inputMax')

        cmds.setAttr(f'{remap_value}.outputMin', 1)
        cmds.setAttr(f'{remap_value}.outputMax', 0)

        # Create attribute
        reader_ah.add_float_attribute(attribute_name=f'output{num}')
        cmds.connectAttr(f'{remap_value}.outValue', f'{ref_reader}.output{num}')


def build_biped_angle_trigger_template():
    """
    Build the angle trigger for each articulation, take into account that you need to change some reference nodes
    position to place it correctly
    """
    # Head
    create_angle_trigger(parent_node='neck_c_skn',
                         driver_node='head_c_skn')
    # Neck
    create_angle_trigger(parent_node='spineTop_c_skn',
                         driver_node='neck_c_skn')
    for side in ('l', 'r'):
        # Clavicle
        create_angle_trigger(parent_node='spineTop_c_skn',
                             driver_node=f'clavicleArm_{side}_skn')
        # UpArm
        create_angle_trigger(parent_node=f'clavicleArm_{side}_skn',
                             driver_node=f'upArm01_{side}_skn')
        # LowArm
        create_angle_trigger(parent_node=cmds.ls(f'upArm??_{side}_jnt')[0],
                             driver_node=f'lowArm01_{side}_skn')
        # hand
        create_angle_trigger(parent_node=cmds.ls(f'lowArm??_{side}_jnt')[0],
                             driver_node=f'handArm_{side}_skn')

        # UpLeg
        create_angle_trigger(parent_node='spineBottom_c_skn',
                             driver_node=f'upLeg01_{side}_skn')
        # LowLeg
        create_angle_trigger(parent_node=cmds.ls(f'upLeg??_{side}_jnt')[0],
                             driver_node=f'lowLeg01_{side}_skn')
        # Foot
        create_angle_trigger(parent_node=cmds.ls(f'lowLeg??_{side}_jnt')[0],
                             driver_node=f'footLeg_{side}_skn')
        # FootMiddle
        create_angle_trigger(parent_node=f'footLeg_{side}_skn',
                             driver_node=f'footLegMiddle_{side}_skn')
