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

    Args:
        driver (str): name of the driver
        driven_list (list): list of driven nodes
        morph_mode (int, optional): 0 == absolute, 1 == relative, 2 == surface, 3 == retarget, 4 == mirror. Defaults to 1.
        morph_space (int, optional): 0 == object space, 1== world space. Defaults to 1.
        use_component_lookup (bool, optional): use component lookup attribute. Defaults to True.
        live_component_match (bool, optional): keep the component match connected. Defaults to False.
        create_component_tag (bool, optional): create the component tag. Defaults to True.

    Returns:
        str: morph's node
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
                             f'{driver_descriptor}{driver_usage}_{driver_side}_morph')
    # Morph attributes
    cmds.setAttr(f'{morph_node}.morphMode', morph_mode)
    cmds.setAttr(f'{morph_node}.morphSpace', morph_space)
    cmds.setAttr(f'{morph_node}.useComponentLookup', use_component_lookup)

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
                                      name=f'{driven_descriptor}_{driven_side}_{usage_lib.component_match}')

        cmds.connectAttr(f'{driver_geo_shape}.{driver_type_connection}',
                         f'{morph_node}.morphTarget[{index}]')

        # Connect geometries to the component match
        cmds.connectAttr(f'{driven_geo_shape_orig}.{driven_type_connection}',
                         f'{cmatch_node}.inputGeometry')
        cmds.connectAttr(f'{driver}.{driver_type_connection}',
                         f'{cmatch_node}.targetGeometry')

        if not live_component_match:
            # Break the component match's live connections
            cmds.disconnectAttr(f'{driven_geo_shape_orig}.{driven_type_connection}',
                                f'{cmatch_node}.inputGeometry')
            cmds.disconnectAttr(f'{driver}.{driver_type_connection}',
                                f'{cmatch_node}.targetGeometry')

        cmds.connectAttr(f'{cmatch_node}.componentLookup',
                         f'{morph_node}.componentLookupList[{index}].componentLookup')

        if create_component_tag:
            # Use the component tag as a mask for the morph
            cmds.connectAttr(f'{cmatch_node}.componentTagExpression',
                             f'{morph_node}.input[{index}].componentTagExpression')

    cmds.optionVar(intValue=('deformationUseComponentTags', deformation_use_component_tags_value))

    return morph_node


def create_component_tag_comparing_two_geometries(driver,
                                                  driven):
    """
    Create a component tag in the driver geometry

    Args:
        driver (str): name of the driver
        driven (str): name of the driven

    Raises:
        RuntimeError: both nodes must be geometries
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
    driven_vertex_len = len(cmds.ls(f'{driven}.{component_type}[*]', flatten=True))
    driver_vertex_len = len(cmds.ls(f'{driver}.{component_type}[*]', flatten=True))

    if driven_vertex_len > driver_vertex_len:
        temp_cmatch = cmds.createNode('componentMatch', name='temp_cmatch')

        cmds.connectAttr(f'{driver}.worldMesh', f'{temp_cmatch}.inputGeometry')
        cmds.connectAttr(f'{driven}.worldMesh', f'{temp_cmatch}.targetGeometry')

        ctag_list = [f'{component_type}[{int(x)}]' for x in
                     cmds.getAttr(f'{temp_cmatch}.componentLookup')[0]]

        cmds.delete(temp_cmatch)

    else:
        ctag_list = [x.split('.')[-1] for x in cmds.ls(f'{driven}.{component_type}[*]', flatten=True)]

    # get the next available index
    component_tag_list = cmds.getAttr(f'{driven}.componentTags', multiIndices=True) or []
    next_free_index = len(component_tag_list) + 1

    # Check if exists a tag with the same name.
    # If exists two componentTags with the same name is not displayed in the attributeEditor.
    for index in component_tag_list:
        existing_tag_name = cmds.getAttr(f'{driven}.componentTags[{index}].componentTagName')
        if driver == existing_tag_name:
            logging.info('Tag is not created because there is already one with the same name.')
            continue

    # Create a new tag with the name and components given
    cmds.setAttr(f'{driven}.componentTags[{next_free_index}].componentTagName', driver,
                 type='string')
    cmds.setAttr(f'{driven}.componentTags[{next_free_index}].componentTagContents',
                 *([len(ctag_list)] + ctag_list), type='componentList')
