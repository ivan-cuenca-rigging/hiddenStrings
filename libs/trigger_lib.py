# Maya imports
from maya import cmds, mel

# Project imports
from hiddenStrings import module_utils
from hiddenStrings.libs import import_export_lib, side_lib, usage_lib, attribute_lib, connection_lib, bifrost_lib


def create_bary(descriptor='bary', side=side_lib.center,
                parent_node=None,
                driver_node=None,
                driver_axis='X'):
    """
    Create a bary trigger with bifrost
    :param descriptor: str
    :param side: str
    :param parent_node: str
    :param driver_node: str
    :param driver_axis: str; X, -X, Y, -Y, Z, -Z
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

    source_file = r'{}/bifrost/{}'.format(module_utils.hidden_strings_path, compound_name)

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
