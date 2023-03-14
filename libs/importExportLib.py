# Imports
import logging
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import jsonLib, skinLib, blendShapeLib


logging = logging.getLogger('hiddenStrings')  # Show module name when using the logging


def export_selection(*args,
                     file_name='storeSelection_data',
                     path=r'{}/temp'.format(os.path.dirname(os.path.dirname(__file__)))):
    """
    Export selection to json
    :param file_name: str
    :param path: str
    """
    if not os.path.exists(path):
        os.makedirs(path)

    selection_data = cmds.ls(selection=True)

    jsonLib.export_data_to_json(data=selection_data,
                                file_name=file_name,
                                file_path=path,
                                relative_path=False)

    logging.info(selection_data)
    return selection_data


def import_selection(*args,
                     path=r'{}/temp/storeSelection_data.json'.format(os.path.dirname(os.path.dirname(__file__)))):
    """
    import selection to json
    :param path: str
    """
    file_name = os.path.basename(path).split('.json')[0]
    path = os.path.dirname(path)

    selection_data = jsonLib.import_data_from_json(file_name=file_name,
                                                   file_path=path,
                                                   relative_path=False)
    cmds.select(selection_data)
    logging.info(selection_data)

    return selection_data


def export_nodes_and_connections(file_name, path, export_nodes=True, export_edges=False, export_connections=True):
    """
    Export nodes and connections to .ma file
    :param file_name: str
    :param path: str
    :param export_nodes: bool
    :param export_edges: bool
    :param export_connections: bool
    """
    node_list = cmds.ls(sl=True)

    cmds.file(r'{}/{}.ma'.format(path, file_name), type='mayaAscii', exportSelectedStrict=True, force=True)

    with open(r'{}/{}.ma'.format(path, file_name), 'r+') as connections_file:
        # Read and store all lines into list
        lines = connections_file.readlines()

        # Move file pointer to the beginning of a file
        connections_file.seek(0)

        # Empty the file
        connections_file.truncate()

        # Get connections and edge nodes
        connections_string = str()
        skip_node_list = list()
        for node in node_list:
            # Get inputs
            inputs_list = cmds.listConnections(node, destination=False, plugs=True, skipConversionNodes=True)
            if inputs_list:
                inputs_list = [x for x in inputs_list if x.split('.')[0] in node_list]
                inputs_list = [(x, cmds.listConnections(x,
                                                        source=False,
                                                        plugs=True,
                                                        skipConversionNodes=True)[0]) for x in inputs_list]
                for value in inputs_list:
                    connections_string += '\nconnectAttr "{}" "{}";'.format(value[0], value[1])

            # Get outputs
            outputs_list = cmds.listConnections(node, source=False, plugs=True, skipConversionNodes=True)
            if outputs_list:
                outputs_list = [x for x in outputs_list if x.split('.')[0] in node_list]
                outputs_list = [(cmds.listConnections(x,
                                                      destination=False,
                                                      plugs=True,
                                                      skipConversionNodes=True)[0], x) for x in outputs_list]

            # Get edges
            if not export_edges:
                if not bool(inputs_list) or not bool(outputs_list):
                    skip_node_list.append(node)

        # ----- Write file -----
        # write createNode lines
        if export_nodes:
            create_node_line_list = [index for index, value in enumerate(lines) if value.startswith('createNode')]
            for create_node_line_index in create_node_line_list:
                node_name = lines[create_node_line_index].split('"')[1]
                if 'unitConversion' not in lines[create_node_line_index]:
                    if node_name not in skip_node_list:
                        connections_file.writelines(lines[create_node_line_index])
                        for line_index, line_value in enumerate(lines[create_node_line_index + 1::]):
                            if line_value.startswith('\t'):
                                if 'rename' not in line_value:
                                    connections_file.writelines(lines[create_node_line_index + line_index + 1])
                            else:
                                break

        # Write connections lines
        if export_connections:
            if len(connections_string) != 0:
                connections_file.writelines(connections_string)

    logging.info(r'{}/{}.ma has been exported'.format(path, file_name))


def import_nodes_and_connections(path, import_nodes=True, import_connections=True):
    """
    Import connections from mel file
    :param path: str
    :param import_nodes: bool
    :param import_connections: bool
    """
    file_name = os.path.basename(path).split('.ma')[0]
    path = os.path.dirname(path)

    with open(r'{}/{}.ma'.format(path, file_name), 'r') as connections_file:
        lines = connections_file.readlines()

        if import_nodes:
            main_line_list = [index for index, value in enumerate(lines) if
                              value.startswith('createNode') or value.startswith('connectAttr')]

            component_range_list = [(value, main_line_list[index + 1]) for index, value in enumerate(main_line_list) if
                                    main_line_list[index] != main_line_list[-1]]

            # Create a temporary mel file to import only the nodes that do not exist in the scene
            with open(r'{}/{}_TEMP.mel'.format(path, file_name), 'w') as connections_file_temp:
                for file_component in component_range_list:
                    if 'createNode' in lines[file_component[0]]:
                        node_name = lines[file_component[0]].split('"')[1]
                        if not cmds.objExists(node_name):
                            for index in range(file_component[0], file_component[1]):
                                connections_file_temp.write(lines[index])
            # Import nodes
            cmds.file(r'{}/{}_TEMP.mel'.format(path, file_name), i=True, force=True)  # i = import
            os.remove(r'{}/{}_TEMP.mel'.format(path, file_name))

        if import_connections:
            # Connect attributes from file, check if the connection exists and force it if false
            for line in lines:
                if line.startswith('connectAttr'):
                    input_value = line.split('"')[1]
                    output_value = line.split('"')[-2]
                    if not cmds.isConnected(input_value, output_value):
                        cmds.connectAttr(input_value, output_value, force=True)

    logging.info(r'{}/{}.ma has been imported'.format(path, file_name))


def export_blend_shape(node, path):
    """
    Export blendShape of the node given
    :param node: str
    :param path: str
    """
    if not cmds.objExists(node):
        cmds.error('{} does not exists in the scene'.format(node))
    blend_shape_name = blendShapeLib.get_blend_shape(node)

    blendShapeLib.check_blendshape(blend_shape=blend_shape_name)
    blend_shape_data = blendShapeLib.get_blend_shape_data(blend_shape_name)

    jsonLib.export_data_to_json(data=blend_shape_data, file_name=blend_shape_name, file_path=path, relative_path=False,
                                compact=True)

    logging.info(r'{}/{}.json has been exported'.format(path, blend_shape_name))


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

    blend_shape = blendShapeLib.get_blend_shape(node=node)
    if blend_shape:
        blend_shape = blendShapeLib.rename_blend_shape(blend_shape=blend_shape)
    else:
        blend_shape = blendShapeLib.create_blend_shape(node=node)

    blend_shape_data = jsonLib.import_data_from_json(file_name=file_name, file_path=path, relative_path=False)
    for target in blend_shape_data['targets']:
        if not blendShapeLib.check_target(blend_shape=blend_shape, target=target):
            blendShapeLib.add_target(blend_shape=blend_shape, target=target)

        target_index = blendShapeLib.get_target_index(blend_shape=blend_shape, target=target)
        for target_value in blend_shape_data['targets'][target]['target_values']:
            points_target = blend_shape_data['targets'][target]['target_values'][target_value]['inputPointsTarget']
            components_target = blend_shape_data[
                                              'targets'][target]['target_values'][target_value]['inputComponentsTarget']
            pretty_target_value = target_value
            target_value = int(float(target_value) * 1000 + 5000)

            if target_value != 6000 and not blendShapeLib.check_in_between(blend_shape=blend_shape,
                                                                           target=target,
                                                                           value=target_value):
                blendShapeLib.add_in_between(blend_shape=blend_shape,
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
            cmds.setAttr('{}.{}'.format(blend_shape, target), blend_shape_data['targets'][target]['envelope'])

    logging.info(r'{}/{}.json has been imported'.format(path, file_name))


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

        import_blend_shape(node=blend_shape_data['node'], path=r'{}/{}'.format(path, blend_shape_file))
    pass


def export_skin_cluster(node, path, skin_index=1):
    """
    Export skinCluster index of the node given if index == None then all index will be exported
    :param node: str
    :param path: str
    :param skin_index: int. -1 (last), 1, 2, 3
    """
    if skin_index:
        skin_cluster = skinLib.rename_skin_cluster(skinLib.get_skin_cluster_index(node, skin_index))
        skin_path = r'{}/{}.json'.format(path, skin_cluster)
        # Check if the file exists and is writable
        if os.path.exists(skin_path) and not os.access(skin_path, os.W_OK):
            cmds.warning('{} is not writeable. Check Permissions'.format(skin_path))
        else:
            # Export JSON
            cmds.deformerWeights('{}.json'.format(skin_cluster), deformer=skin_cluster, method='index',
                                 export=True, format='JSON', path=path)
    else:
        skin_cluster_list = skinLib.get_skin_cluster_list(node)
        for skin_cluster in skin_cluster_list:
            skin_cluster = skinLib.rename_skin_cluster(skin_cluster)
            skin_path = r'{}/{}.json'.format(path, skin_cluster)
            # Check if the file exists and is writable
            if os.path.exists(skin_path) and not os.access(skin_path, os.W_OK):
                cmds.warning('{} is not writeable. Check Permissions'.format(skin_path))
            else:
                # Export skinCluster JSON
                cmds.deformerWeights('{}.json'.format(skin_cluster), deformer=skin_cluster, method='index',
                                     export=True, format='JSON', path=path)


def export_skin_clusters(node_list, path, skin_index=1):
    """
    export all skinClusters
    :param node_list: list
    :param path: string
    :param skin_index: int. -1 (last), 1, 2, 3
    """
    for node in node_list:
        export_skin_cluster(node=node, path=path, skin_index=skin_index)


def import_skin_cluster(node, path, skin_index=1, import_method='index'):
    """
    Import skinCluster from path
    :param node: str
    :param path: str
    :param skin_index: int. -1 (last), 1, 2, 3
    :param import_method: index or nearest
    :return:
    """
    skin_cluster = skinLib.get_skin_cluster_index(node, skin_index)
    file_name = os.path.basename(path)
    path = os.path.dirname(path)

    # Get json file joints
    skin_data = jsonLib.import_data_from_json(file_name=file_name.split('.')[0],
                                              file_path=path,
                                              relative_path=False)
    file_skin_joints = list()
    for value in skin_data['deformerWeight']['weights']:
        file_skin_joints.append(value['source'])

    # Check if the joints exists in the scene
    joints_not_in_scene = list()
    for jnt in file_skin_joints:
        if not cmds.objExists(jnt):
            joints_not_in_scene.append(jnt)
    if len(joints_not_in_scene) > 0:
        cmds.error('missing in the scene: {}'.format(joints_not_in_scene))

    # If skinCluster exists get its joints and add the joints that are not in the skinCluster
    if skin_cluster:
        skin_cluster_joints = cmds.skinCluster(skin_cluster, query=True, influence=True)
        joints_to_add = [x for x in file_skin_joints if x not in skin_cluster_joints]

        cmds.skinCluster(skin_cluster, edit=True, addInfluence=joints_to_add, lockWeights=True)
        skinLib.rename_skin_cluster(skin_cluster)

    # If skinCluster does not exist create it
    else:
        skin_cluster = skinLib.create_skin_cluster(joints=file_skin_joints, node=node, skin_index=skin_index)

    # Import skinCluster JSON
    cmds.deformerWeights(file_name, path=path, deformer=skin_cluster,
                         im=True, edit=True, method=import_method)

    logging.info('{} has been imported'.format(file_name))


def import_skin_clusters(path, import_method='index'):
    """
    Import all json skinClusters from folder
    :param path: string
    :param import_method: string, index or nearest
    """
    file_list = [x for x in os.listdir(path) if x.endswith('.json')]
    for skin_file in file_list:
        # Get json file node
        skin_data = jsonLib.import_data_from_json(file_name=skin_file.split('.')[0],
                                                  file_path=path,
                                                  relative_path=False)

        node = cmds.listRelatives(skin_data['deformerWeight']['shapes'][0]['name'], parent=True)[0]
        skin_cluster = skin_data['deformerWeight']['weights'][0]['deformer']
        skin_index = int(skin_cluster.split('_')[0][-2:])

        import_skin_cluster(node=node, path=r'{}/{}'.format(path, skin_file),
                            skin_index=skin_index, import_method=import_method)
