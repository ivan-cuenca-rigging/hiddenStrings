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
    :param descriptor: str
    :param side: str
    :param parent_node: str
    :param driver_node: str
    """
    bary_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(descriptor,
                                                                     usage_lib.get_usage_capitalize(usage_lib.trigger),
                                                                     side,
                                                                     usage_lib.group))

    # Create Bary geometry
    bary_geo = import_export_lib.import_obj(
        path=r'{}/libs/geo_shapes/bary.obj'.format(module_utils.hidden_strings_path))[0]
    bary_geo = cmds.rename(bary_geo, '{}_{}_{}'.format(descriptor, side, usage_lib.geometry))
    bary_geo_shape = cmds.listRelatives(bary_geo, allDescendents=True, shapes=True, noIntermediate=True)[0]

    # Create bary node (bifrost graph)
    compound_namespace = 'rigging'
    compound_name = 'barycentricPoseReader'

    source_file = r'{}/bifrost/{}.json'.format(module_utils.hidden_strings_path, compound_name)

    bifrost_lib.copy_bifrost_compound(source_file=source_file, destination_dir=bifrost_lib.bifrost_path, force=True)

    bary_shape = bifrost_lib.import_compound(compound_namespace=compound_namespace, compound_name=compound_name)
    bary_trigger = cmds.rename(cmds.listRelatives(bary_shape, parent=True)[0],
                               '{}_{}_{}'.format(descriptor, side, usage_lib.trigger))
    bary_shape = cmds.listRelatives(bary_trigger, allDescendents=True, shapes=True, noIntermediate=True)[0]

    cmds.parent(bary_geo, bary_trigger)
    cmds.parent(bary_geo_shape, bary_trigger, relative=True, shape=True)
    cmds.delete(bary_geo)

    cmds.parent(bary_trigger, bary_grp)

    # Create driver
    driver_shape = cmds.createNode('locator', name='{}_{}_{}Shape'.format(descriptor, side, usage_lib.driver))
    driver = cmds.rename(cmds.listRelatives(driver_shape, parent=True)[0],
                         '{}_{}_{}'.format(descriptor, side, usage_lib.driver))
    cmds.parent(driver, bary_grp)

    for axis in 'XYZ':
        cmds.setAttr('{}.localScale{}'.format(driver_shape, axis), 0.25)
    # Connect driver and shape to the bary node
    cmds.connectAttr('{}.worldMesh'.format(bary_geo_shape), '{}.mesh'.format(bary_shape))
    cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.driverMatrix'.format(bary_shape))

    # Create outputs
    vertex_length = len(cmds.ls('{}.vtx[*]'.format(bary_geo_shape), flatten=True))

    driver_ah = attribute_lib.Helper(driver)

    driver_ah.lock_and_hide_attributes(attributes_list=['scaleX', 'scaleY', 'scaleZ',
                                                        'visibility'])
    driver_ah.add_separator_attribute(separator_name='Attributes')

    driver_ah.add_enum_attribute(attribute_name='driverAxis', states='X:-X:Y:-Y:Z:-Z', keyable=False)
    cmds.connectAttr('{}.driverAxis'.format(driver), '{}.driverAxis'.format(bary_shape))
    driver_ah.add_separator_attribute(separator_name='Weights')
    weight_attribute = 'weight'
    for index in range(vertex_length):
        driver_ah.add_float_attribute(attribute_name='{}{}'.format(weight_attribute, str(index)))
        cmds.connectAttr('{}.baryWeight[{}]'.format(bary_shape, str(index)),
                         '{}.{}{}'.format(driver, weight_attribute, str(index)))

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
    :param parent_node: str
    :param driver_node: str
    :param forbidden_word: str
    :param structural_parent: str
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
    angle_reader_group = cmds.createNode('transform', name='{}AngleReader_{}_grp'.format(descriptor, side),
                                         parent=structural_parent)

    cmds.xform(angle_reader_group, worldSpace=True,
               matrix=cmds.xform(driver_node, query=True, worldSpace=True, matrix=True))

    connection_lib.connect_offset_parent_matrix(driver=parent_node, driven=angle_reader_group)

    # Create the reader
    ref_reader = cmds.createNode('transform', name='{}Reader_{}_{}'.format(descriptor, side, usage_lib.reference),
                                 parent=angle_reader_group)
    ref_reader_static = cmds.createNode('transform',
                                        name='{}ReaderStatic_{}_{}'.format(descriptor, side, usage_lib.reference),
                                        parent=angle_reader_group)

    # Give the position to the reader
    reader_mult_mat = cmds.createNode('multMatrix',
                                      name='{}ReaderRef_{}_{}'.format(driver_node, side, usage_lib.mult_matrix))

    cmds.connectAttr('{}.worldMatrix'.format(driver_node), '{}.matrixIn[0]'.format(reader_mult_mat))
    cmds.connectAttr('{}.worldInverseMatrix'.format(parent_node), '{}.matrixIn[1]'.format(reader_mult_mat))
    cmds.setAttr('{}.matrixIn[2]'.format(reader_mult_mat),
                 cmds.getAttr('{}.worldMatrix'.format(parent_node)), type='matrix')
    cmds.setAttr('{}.matrixIn[3]'.format(reader_mult_mat),
                 cmds.getAttr('{}.worldInverseMatrix'.format(driver_node)), type='matrix')

    cmds.connectAttr('{}.matrixSum'.format(reader_mult_mat), '{}.offsetParentMatrix'.format(ref_reader))
    cmds.setAttr('{}.translateX'.format(ref_reader), 1)
    cmds.setAttr('{}.translateX'.format(ref_reader_static), 1)

    cmds.setAttr('{}.displayHandle'.format(ref_reader), 1)
    cmds.setAttr('{}.displayHandle'.format(ref_reader_static), 1)

    # Create a vector for the reader
    vector_reader_pma = vector_lib.create_pma_vector_from_a_to_b(a=angle_reader_group, b=ref_reader)
    vector_reader_static_pma = vector_lib.create_pma_vector_from_a_to_b(a=angle_reader_group, b=ref_reader_static)

    # Create attribute helper and separator
    reader_ah = attribute_lib.Helper(ref_reader)
    reader_ah.add_separator_attribute(separator_name='Outputs')

    for num in ['01', '02', '03', '04']:
        # Create a reader in each direction
        ref_transform = cmds.createNode('transform',
                                        name='{}Reader{}_{}_{}'.format(descriptor, num, side, usage_lib.reference),
                                        parent=angle_reader_group)

        # Give the position to each transform
        axis = 'Y' if num == '01' or num == '03' else 'Z'
        value = 1 if num == '01' or num == '02' else -1

        cmds.setAttr('{}.translate{}'.format(ref_transform, axis), value)
        cmds.setAttr('{}.displayHandle'.format(ref_transform), 1)

        # Create a vector for each direction
        vector_pma = vector_lib.create_pma_vector_from_a_to_b(a=angle_reader_group, b=ref_transform)

        # Create an angle between for each direction
        angle_between = vector_lib.create_angle_between_two_pma_nodes(vector_pma, vector_reader_pma)
        angle_between_static = vector_lib.create_angle_between_two_pma_nodes(vector_pma, vector_reader_static_pma)

        # Remap values to normalize the outputs
        remap_value = cmds.createNode('remapValue',
                                      name='{}Reader{}_{}_{}'.format(descriptor, num, side, usage_lib.remap_value))

        cmds.connectAttr(angle_between, '{}.inputValue'.format(remap_value))
        cmds.connectAttr(angle_between_static, '{}.inputMax'.format(remap_value))

        cmds.setAttr('{}.outputMin'.format(remap_value), 1)
        cmds.setAttr('{}.outputMax'.format(remap_value), 0)

        # Create attribute
        reader_ah.add_float_attribute(attribute_name='output{}'.format(num))
        cmds.connectAttr('{}.outValue'.format(remap_value), '{}.output{}'.format(ref_reader, num))


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
                             driver_node='clavicleArm_{}_skn'.format(side))
        # UpArm
        create_angle_trigger(parent_node='clavicleArm_{}_skn'.format(side),
                             driver_node='upArm01_{}_skn'.format(side))
        # LowArm
        create_angle_trigger(parent_node=cmds.ls('upArm??_{}_jnt'.format(side))[0],
                             driver_node='lowArm01_{}_skn'.format(side))
        # hand
        create_angle_trigger(parent_node=cmds.ls('lowArm??_{}_jnt'.format(side))[0],
                             driver_node='handArm_{}_skn'.format(side))

        # UpLeg
        create_angle_trigger(parent_node='spineBottom_c_skn',
                             driver_node='upLeg01_{}_skn'.format(side))
        # LowLeg
        create_angle_trigger(parent_node=cmds.ls('upLeg??_{}_jnt'.format(side))[0],
                             driver_node='lowLeg01_{}_skn'.format(side))
        # Foot
        create_angle_trigger(parent_node=cmds.ls('lowLeg??_{}_jnt'.format(side))[0],
                             driver_node='footLeg_{}_skn'.format(side))
        # FootMiddle
        create_angle_trigger(parent_node='footLeg_{}_skn'.format(side),
                             driver_node='footLegMiddle_{}_skn'.format(side))
