# Maya imports
from maya import cmds, mel

# Project imports
from hiddenStrings import module_utils
from hiddenStrings.libs import import_export_lib, side_lib, usage_lib, attribute_lib


def create_bary(name='bary', side=side_lib.center):
    """
    Create a bary trigger with bifrost
    :param name: str
    :param side: str
    """
    bary_grp = cmds.createNode('transform', name='{}{}_{}_{}'.format(name,
                                                                     usage_lib.get_usage_capitalize(usage_lib.trigger),
                                                                     side,
                                                                     usage_lib.group))

    # Create Bary geometry
    bary_geo = import_export_lib.import_obj(
        path=r'{}/libs/geo_shapes/bary.obj'.format(module_utils.hidden_strings_path))[0]
    bary_geo = cmds.rename(bary_geo, '{}_{}_{}'.format(name, side, usage_lib.geometry))
    bary_geo_shape = cmds.listRelatives(bary_geo, allDescendents=True, shapes=True, noIntermediate=True)[0]

    # Create bary node (bifrost graph)
    bary_shape = mel.eval('bifrostGraph -importGraphAsShape "hiddenStrings::bary"')
    bary_trigger = cmds.rename(cmds.listRelatives(bary_shape, parent=True)[0],
                               '{}_{}_{}'.format(name, side, usage_lib.trigger))
    bary_shape = cmds.listRelatives(bary_trigger, allDescendents=True, shapes=True, noIntermediate=True)[0]

    cmds.parent(bary_geo, bary_trigger)
    cmds.parent(bary_geo_shape, bary_trigger, relative=True, shape=True)
    cmds.delete(bary_geo)

    cmds.parent(bary_trigger, bary_grp)

    # Create driver
    driver_shape = cmds.createNode('locator', name='{}_{}_{}Shape'.format(name, side, usage_lib.driver))
    driver = cmds.rename(cmds.listRelatives(driver_shape, parent=True)[0],
                         '{}_{}_{}'.format(name, side, usage_lib.driver))
    cmds.parent(driver, bary_grp)

    # Connect driver and shape to the bary node
    cmds.connectAttr('{}.worldMesh'.format(bary_geo_shape), '{}.mesh'.format(bary_shape))
    cmds.connectAttr('{}.worldMatrix'.format(driver), '{}.driverMatrix'.format(bary_shape))

    # Create outputs
    vertex_length = len(cmds.ls('{}.vtx[*]'.format(bary_geo_shape), flatten=True))

    driver_ah = attribute_lib.Helper(driver)

    driver_ah.lock_and_hide_attributes(attributes_list=['scaleX', 'scaleY', 'scaleZ',
                                                        'visibility'])
    driver_ah.add_separator_attribute(separator_name='Attributes')
    weight_attribute = 'weight'
    for index in range(vertex_length):
        driver_ah.add_float_attribute(attribute_name='{}{}'.format(weight_attribute, str(index)))
        cmds.connectAttr('{}.baryWeight[{}]'.format(bary_shape, str(index)),
                         '{}.{}{}'.format(driver, weight_attribute, str(index)))
