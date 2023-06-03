# Imports
import logging
# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import side_lib, usage_lib

logging = logging.getLogger(__name__)


def create_morph_deformer(driver,
                          driven_list,
                          morph_mode=1,
                          morph_space=1,
                          use_component_lookup=True,
                          live_component_match=False,
                          create_component_tag=True):
    """
    Create a morph deformer connection
    :param driver: str
    :param driven_list: list
    :param morph_mode: int
    :param morph_space: int
    :param use_component_lookup: bool
    :param live_component_match: bool
    :param create_component_tag: bool
    :return: morph deformer
    """
    # CHECKS
    deformation_use_component_tags_value = cmds.optionVar(query='deformationUseComponentTags')
    if not deformation_use_component_tags_value:
        cmds.optionVar(intValue=('deformationUseComponentTags', True))

    if len(driver.split('_')) == 3:
        driver_descriptor, driver_side, driver_usage = driver.split('_')
    else:
        driver_descriptor = driver
        driver_side = side_lib.center
        driver_usage = usage_lib.test

    driver_geo_shape = cmds.listRelatives(driver, children=True, shapes=True, noIntermediate=True)[0]
    driver_type = cmds.objectType(driver_geo_shape)
    driver_type_connection = 'worldMesh'
    if 'nurbs' in driver_type:
        driver_type_connection = 'worldSpace'
    if 'lattice' in driver_type:
        driver_type_connection = 'worldLattice'

    # Create a component tag for the vertex that match in both geometries
    if create_component_tag:
        for driven in driven_list:
            create_component_tag_comparing_two_geometries(driver=driver, driven=driven)

    # Create the morph deformer
    morph_node = cmds.rename(cmds.deformer(driven_list, type='morph'),
                             '{}{}_{}_morph'.format(driver_descriptor, driver_usage, driver_side))
    # Morph attributes
    cmds.setAttr('{}.morphMode'.format(morph_node), morph_mode)
    cmds.setAttr('{}.morphSpace'.format(morph_node), morph_space)
    cmds.setAttr('{}.useComponentLookup'.format(morph_node), use_component_lookup)

    # For each driven
    for index, driven in enumerate(driven_list):
        if len(driver.split('_')) == 3:
            driven_descriptor, driven_side, driven_usage = driven.split('_')
        else:
            driven_descriptor = driver
            driven_side = side_lib.center

        driven_geo_shape_orig = cmds.listRelatives(driven, children=True, shapes=True, noIntermediate=False)[-1]
        driven_type = cmds.objectType(driven_geo_shape_orig)
        driven_type_connection = 'worldMesh'
        if 'nurbs' in driven_type:
            driven_type_connection = 'worldSpace'
        if 'lattice' in driven_type:
            driven_type_connection = 'worldLattice'

        # Connections needed for the morph that cmds.deformer(type='morph') does not create
        cmatch_node = cmds.createNode('componentMatch',
                                      name='{}_{}_{}'.format(driven_descriptor, driven_side, usage_lib.component_match))

        cmds.connectAttr('{}.{}'.format(driver_geo_shape, driver_type_connection),
                         '{}.morphTarget[{}]'.format(morph_node, index))

        # Connect geometries to the component match
        cmds.connectAttr('{}.{}'.format(driven_geo_shape_orig, driven_type_connection),
                         '{}.inputGeometry'.format(cmatch_node))
        cmds.connectAttr('{}.{}'.format(driver, driver_type_connection),
                         '{}.targetGeometry'.format(cmatch_node))

        if not live_component_match:
            # Break the component match's live connections
            cmds.disconnectAttr('{}.{}'.format(driven_geo_shape_orig, driven_type_connection),
                                '{}.inputGeometry'.format(cmatch_node))
            cmds.disconnectAttr('{}.{}'.format(driver, driver_type_connection),
                                '{}.targetGeometry'.format(cmatch_node))

        cmds.connectAttr('{}.componentLookup'.format(cmatch_node),
                         '{}.componentLookupList[{}].componentLookup'.format(morph_node, index))

        if create_component_tag:
            # Use the component tag as a mask for the morph
            cmds.setAttr('{}.input[{}].componentTagExpression'.format(morph_node, index), driver, type='string')

    cmds.optionVar(intValue=('deformationUseComponentTags', deformation_use_component_tags_value))

    return morph_node


def create_component_tag_comparing_two_geometries(driver,
                                                  driven):
    """
    Create a component tag in the driver geometry
    :param driver: str
    :param driven: str
    """
    # Maya imports
    from maya import cmds

    # Checks
    driver_type = cmds.objectType(cmds.listRelatives(driver, children=True, shapes=True, noIntermediate=True)[0])
    driven_type = cmds.objectType(cmds.listRelatives(driven, children=True, shapes=True, noIntermediate=True)[0])
    component_type = 'vtx'

    if driver_type != 'mesh' or driven_type != 'mesh':
        raise RuntimeError('Both, driver and driven, must be objects of type mesh (geometries),'
                           'If they are not meshes create_component_tag must be set to False')

        # Compare both geometries, if driven is bigger than driver we need to create a temporal componentMatch
    driven_vertex_len = len(cmds.ls('{}.{}[*]'.format(driven, component_type), flatten=True))
    driver_vertex_len = len(cmds.ls('{}.{}[*]'.format(driver, component_type), flatten=True))

    if driven_vertex_len > driver_vertex_len:
        temp_cmatch = cmds.createNode('componentMatch', name='temp_cmatch')

        cmds.connectAttr('{}.worldMesh'.format(driver), '{}.inputGeometry'.format(temp_cmatch))
        cmds.connectAttr('{}.worldMesh'.format(driven), '{}.targetGeometry'.format(temp_cmatch))

        ctag_list = ['{}[{}]'.format(component_type, int(x)) for x in
                     cmds.getAttr('{}.componentLookup'.format(temp_cmatch))[0]]

        cmds.delete(temp_cmatch)

    else:
        ctag_list = [x.split('.')[-1] for x in cmds.ls('{}.{}[*]'.format(driven, component_type), flatten=True)]

    # get the next available index
    component_tag_list = cmds.getAttr('{}.componentTags'.format(driven), multiIndices=True) or []
    next_free_index = len(component_tag_list) + 1

    # Check if exists a tag with the same name.
    # If exists two componentTags with the same name is not displayed in the attributeEditor.
    for index in component_tag_list:
        existing_tag_name = cmds.getAttr('{}.componentTags[{}].componentTagName'.format(driven, index))
        if driver == existing_tag_name:
            logging.info('Tag is not created because there is already one with the same name.')
            continue

    # Create a new tag with the name and components given
    cmds.setAttr('{}.componentTags[{}].componentTagName'.format(driven, next_free_index), driver,
                 type='string')
    cmds.setAttr('{}.componentTags[{}].componentTagContents'.format(driven, next_free_index),
                 *([len(ctag_list)] + ctag_list), type='componentList')
