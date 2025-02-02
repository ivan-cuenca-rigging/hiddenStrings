# Imports
import json
import os
import logging

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import skin_lib, blend_shape_lib

logging = logging.getLogger(__name__)


def export_selection(file_name, path):
    """
    Expport selection to json

    Args:
        file_name (str): name of the file
        path (str): export file folder

    Returns:
        list: selection list exported to the file
    """
    if not os.path.exists(path):
        os.makedirs(path)

    selection_data = cmds.ls(selection=True)

    export_data_to_json(data=selection_data,
                        file_name=file_name,
                        file_path=path,
                        relative_path=False)

    logging.info(selection_data)
    return selection_data


def import_selection(path):
    """
    Import selection from json

    Args:
        path (str): full path of the file to import

    Returns:
        list: selection list imported from the file
    """
    file_name = os.path.basename(path).split('.json')[0]
    path = os.path.dirname(path)

    selection_data = import_data_from_json(file_name=file_name,
                                           file_path=path,
                                           relative_path=False)
    cmds.select(selection_data)
    logging.info(selection_data)

    return selection_data


def export_matrix(file_name, path):
    """
    Expport matrix to json

    Args:
        file_name (str): name of the file
        path (str): export file folder

    Returns:
        matrix: matrix exported to the file
    """
    if not os.path.exists(path):
        os.makedirs(path)

    matrix_data = cmds.xform(cmds.ls(selection=True)[0], query=True, worldSpace=True, matrix=True)

    export_data_to_json(data=matrix_data,
                        file_name=file_name,
                        file_path=path,
                        relative_path=False)

    logging.info(matrix_data)
    return matrix_data


def import_matrix(path):
    """
    Import matrix from json

    Args:
        path (str): full path of the file to import

    Returns:
        matrix: matrix imported from the file
    """
    file_name = os.path.basename(path).split('.json')[0]
    path = os.path.dirname(path)

    matrix_data = import_data_from_json(file_name=file_name,
                                        file_path=path,
                                        relative_path=False)
    cmds.xform(cmds.ls(selection=True)[0], worldSpace=True, matrix=matrix_data)
    logging.info(matrix_data)

    return matrix_data


def export_nodes_and_connections(file_name, path, export_nodes=True, export_edges=False, export_connections=True):
    """
    Export nodes and connections to an .ma file

    Args:
        file_name (str): name of the file
        path (str): export file folder
        export_nodes (bool, optional): True == export nodes. Defaults to True.
        export_edges (bool, optional): True == export edges. Defaults to False.
        export_connections (bool, optional): True == export connections. Defaults to True.
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

                for input_value in inputs_list:
                    output_value = [x for x in cmds.listConnections(input_value, plugs=True, source=True,
                                                                    skipConversionNodes=True)
                                    if node in x][0]
                    connections_string += f'\nconnectAttr "{input_value}" "{output_value}";'

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

    logging.info(r'{}/{}.ma has been exported.'.format(path, file_name))


def import_nodes_and_connections(path, import_nodes=True, import_connections=True, search_for=None, replace_with=None):
    """
    Import connections from mel file

    Args:
        path (_type_): full path of the file to import
        import_nodes (bool, optional): True == import nodes. Defaults to True.
        import_connections (bool, optional): True == import connections. Defaults to True.
        search_for (_type_, optional): search string. Use "," for more than once. Defaults to None.
        replace_with (_type_, optional): replace string. Use "," for more than once. Defaults to None.
    """
    if search_for:
        search_and_replace_in_file(path, search_for=search_for, replace_with=replace_with)

    with open(path, 'r') as connections_file:
        lines = connections_file.readlines()

        if import_nodes:
            main_line_list = [index for index, value in enumerate(lines) if
                              value.startswith('createNode') or value.startswith('connectAttr')]

            component_range_list = [(value, main_line_list[index + 1]) for index, value in enumerate(main_line_list) if
                                    main_line_list[index] != main_line_list[-1]]

            # Create a temporary mel file to import only the nodes that do not exist in the scene
            with open(r'{}_TEMP.mel'.format(path.split('.ma')[0]), 'w') as connections_file_temp:
                for file_component in component_range_list:
                    if 'createNode' in lines[file_component[0]]:
                        node_name = lines[file_component[0]].split('"')[1]
                        if not cmds.objExists(node_name):
                            for index in range(file_component[0], file_component[1]):
                                connections_file_temp.write(lines[index])
            # Import nodes
            cmds.file(r'{}_TEMP.mel'.format(path.split('.ma')[0]), i=True, force=True)  # i = import
            os.remove(r'{}_TEMP.mel'.format(path.split('.ma')[0]))

        # Connect attributes from file, check if the connection exists and force it if false
        if import_connections:
            for line in lines:
                if line.startswith('connectAttr'):
                    input_value = line.split('"')[1]
                    output_value = line.split('"')[-2]
                    if not cmds.isConnected(input_value, output_value):
                        cmds.connectAttr(input_value, output_value, force=True)

    if search_for:
        search_and_replace_in_file(path, search_for=replace_with, replace_with=search_for)

    logging.info(r'{} has been imported.'.format(path))


def import_obj(path):
    """
    Import obj

    Args:
        path (str): full path of the file to import

    Returns:
        str: file path
    """
    return cmds.file(path, type='OBJ', i=True, force=True, returnNewNodes=True)  # i = import


def export_blend_shape(node, path):
    """
    Export blendShape of the node given

    Args:
        node (str): node of the node deformed by the blendshape we want to export
        path (str): export file folder
    """
    if not cmds.objExists(node):
        cmds.error(f'{node} does not exists in the scene')
    blend_shape_name = blend_shape_lib.get_blend_shape(node)

    blend_shape_lib.check_blendshape(blend_shape=blend_shape_name)
    blend_shape_data = blend_shape_lib.get_blend_shape_data(blend_shape_name)

    if not os.path.exists(path):
        os.makedirs(path)

    export_data_to_json(data=blend_shape_data, file_name=blend_shape_name, file_path=path, relative_path=False,
                        compact=True)

    logging.info(r'{}/{}.json has been exported.'.format(path, blend_shape_name))


def export_blend_shapes(node_list, path):
    """
    Export blendShapes of the nodes given

    Args:
        node_list (list): list of nodes deformed by the blendshapes we want to export
        path (str): export file folder
    """
    for node in node_list:
        export_blend_shape(node=node, path=path)


def import_blend_shape(node, path):
    """
    Import blendShape from path

    Args:
        node (str): node that receives the blendshape
        path (str): full file path to import
    """
    file_name = os.path.basename(path).split('.json')[0]
    path = os.path.dirname(path)

    blend_shape = blend_shape_lib.get_blend_shape(node=node)
    if blend_shape:
        blend_shape = blend_shape_lib.rename_blend_shape(blend_shape=blend_shape)
    else:
        blend_shape = blend_shape_lib.create_blend_shape(node=node)

    blend_shape_data = import_data_from_json(file_name=file_name, file_path=path, relative_path=False)

    blend_shape_lib.set_blendshape_data(blend_shape=blend_shape, blend_shape_data=blend_shape_data)

    logging.info(r'{}/{}.json has been imported.'.format(path, file_name))


def import_blend_shapes(path):
    """
    Import all json blendShapes from folder

    Args:
        path (str): folder path to import
    """
    file_list = [x for x in os.listdir(path) if x.endswith('.json')]
    for blend_shape_file in file_list:
        # Get json file node
        blend_shape_data = import_data_from_json(file_name=blend_shape_file.split('.')[0],
                                                 file_path=path,
                                                 relative_path=False)

        import_blend_shape(node=blend_shape_data['node'], path=r'{}/{}'.format(path, blend_shape_file))
    pass


def export_skin_cluster(node, path, skin_index=1):
    """
    Export node skinCluster/s
    
    Args:
        node (str): node with a skinCluster
        path (str): export file folder
        skin_index (int): index of the skin, if None all the skinClusters will be exported. Defaults to 1.
    """
    if skin_index:
        skin_cluster = skin_lib.rename_skin_cluster(skin_lib.get_skin_cluster_index(node, skin_index))
        skin_path = r'{}/{}.json'.format(path, skin_cluster)
        # Check if the file exists and is writable
        if os.path.exists(skin_path) and not os.access(skin_path, os.W_OK):
            logging.info(f'{skin_path} is not writeable. Check Permissions.')
        else:
            if not os.path.exists(path):
                os.makedirs(path)
            # Export JSON
            cmds.deformerWeights(f'{skin_cluster}.json', deformer=skin_cluster, method='index',
                                 export=True, format='JSON', path=path)
    else:
        skin_cluster_list = skin_lib.get_skin_cluster_list(node)
        for skin_cluster in skin_cluster_list:
            skin_cluster = skin_lib.rename_skin_cluster(skin_cluster)
            skin_path = r'{}/{}.json'.format(path, skin_cluster)
            # Check if the file exists and is writable
            if os.path.exists(skin_path) and not os.access(skin_path, os.W_OK):
                logging.info(f'{skin_path} is not writeable. Check Permissions.')
            else:
                if not os.path.exists(path):
                    os.makedirs(path)
                # Export skinCluster JSON
                cmds.deformerWeights(f'{skin_cluster}.json', deformer=skin_cluster, method='index',
                                     export=True, format='JSON', path=path)


def export_skin_clusters(node_list, path, skin_index=1):
    """
    Export all skinClusters

    Args:
        node_list (list): list of nodes with the skinClusters we want to export
        path (str): export folder path
        skin_index (int): index of the skin, if None all the skinClusters will be exported. Defaults to 1.
    """
    for node in node_list:
        export_skin_cluster(node=node, path=path, skin_index=skin_index)


def import_skin_cluster(node, path, skin_index=1, import_method='index', search_for=None, replace_with=None):
    """
    Import skinCluster from path

    Args:
        node (str): node that receives the skinCluster
        path (str): full path of the skinCluster to import
        skin_index (int): index of the skin, if None all the skinClusters will be exported. Defaults to 1.
        import_method (str): index or nearest. Defaults to 'index'.
        search_for (str): search string. Use ',' for more than once
        replace_with (str): replace string. Use ',' for more than once
    """
    skin_cluster = skin_lib.get_skin_cluster_index(node, skin_index)
    file_name = os.path.basename(path)
    path = os.path.dirname(path)

    if search_for:
        search_and_replace_in_file(r'{}/{}'.format(path, file_name), search_for=search_for, replace_with=replace_with)

    # Get json file joints
    skin_data = import_data_from_json(file_name=file_name.split('.')[0],
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
        cmds.error(f'missing in the scene: {joints_not_in_scene}')

    # If skinCluster exists get its joints and add the joints that are not in the skinCluster
    joints_to_lock = list()
    if skin_cluster:
        skin_cluster_joints = cmds.skinCluster(skin_cluster, query=True, influence=True)

        joints_to_add = [x for x in file_skin_joints if x not in skin_cluster_joints]
        joints_to_lock = [x for x in skin_cluster_joints if x not in file_skin_joints]

        cmds.skinCluster(skin_cluster, edit=True, addInfluence=joints_to_add, lockWeights=True)

    # If skinCluster does not exist create it
    else:
        skin_cluster = skin_lib.create_skin_cluster(joints=file_skin_joints, node=node, skin_index=skin_index)

    # Reading normalize weights
    skin_normalize = cmds.skinCluster(skin_cluster, query=True, normalizeWeights=True)
    # disable normalize weights
    cmds.skinCluster(skin_cluster, edit=True, normalizeWeights=0)

    # Empty skin cluster, if not it does not work as expected
    node_type = cmds.nodeType(cmds.listRelatives(node, shapes=True)[0])
    if 'nurbs' in node_type:
        component_type = 'cv'
    elif 'lattice' in node_type:
        component_type = 'pt'
    else:
        component_type = 'vtx'

    shape_components = f'{cmds.listRelatives(node, shapes=True, noIntermediate=True)[0]}.{component_type}[:]'

    cmds.skinPercent(skin_cluster, shape_components, normalize=False, pruneWeights=100)
    if joints_to_lock:
        for jnt in joints_to_lock:
            cmds.skinCluster(skin_cluster, edit=True, influence=jnt, lockWeights=True)

    # Import skinCluster
    try:
        cmds.deformerWeights(file_name, path=path, deformer=skin_cluster, im=True, method=import_method)
    except:
        logging.warning(f'{skin_cluster} has not been imported, check the topology')

    # Restore normalize weights
    cmds.skinCluster(skin_cluster, edit=True, normalizeWeights=skin_normalize)
    cmds.skinCluster(skin_cluster, edit=True, forceNormalizeWeights=True)

    if search_for:
        search_and_replace_in_file(r'{}/{}'.format(path, file_name), search_for=replace_with, replace_with=search_for)

    logging.info(f'{file_name} has been imported.')


def import_skin_clusters(path, import_method='index'):
    """
    Import all json skinClusters from folder

    Args:
        path (str): 
        import_method (str): can be 'index' or 'nearest'
    """
    file_list = [x for x in os.listdir(path) if x.endswith('.json')]
    for skin_file in file_list:
        # Get json file node
        skin_data = import_data_from_json(file_name=skin_file.split('.')[0],
                                          file_path=path,
                                          relative_path=False)

        node = cmds.listRelatives(skin_data['deformerWeight']['shapes'][0]['name'], parent=True)[0]
        skin_cluster = skin_data['deformerWeight']['weights'][0]['deformer']
        skin_index = int(skin_cluster.split('_')[0][-1:])

        import_skin_cluster(node=node, path=r'{}/{}'.format(path, skin_file),
                            skin_index=skin_index, import_method=import_method)


def export_data_to_json(data, file_name, file_path, relative_path=True, use_indent=True, compact=False):
    """
    export data to a json file

    Args:
        data (str): data to export
        file_name (str): file name
        file_path (str): file folder path
        relative_path (bool): relative to the file. Defaults to True
        use_indent (bool): indentation. Defaults to True
        compact (bool): for huge files. Defaults to False

    Returns: 
        str: file path name with ".json"
    """
    if relative_path:
        module_path = os.path.dirname(os.path.dirname(__file__))
        file_path_name_with_extension = f'{module_path}/{file_path}/{file_name}.json'
    else:
        file_path_name_with_extension = f'{file_path}/{file_name}.json'

    if compact:
        with open(file_path_name_with_extension, 'w') as write_file:
            json.dump(data, write_file)
    else:
        with open(file_path_name_with_extension, 'w') as write_file:
            indent_value = 4 if use_indent else 0
            json.dump(data, write_file, indent=indent_value)

    return file_path_name_with_extension


def import_data_from_json(file_name, file_path, relative_path=True):
    """
    Import data from a json file

    Args:
        file_name (str): file name
        file_path (str): file folder path
        relative_path (bool): relative to the file. Defaults to True

    Returns:
        str: data imported
    """
    if relative_path:
        script_path = os.path.dirname(os.path.dirname(__file__))
        file_path_name_with_extension = f'{script_path}/{file_path}/{file_name}.json'
    else:
        file_path_name_with_extension = f'{file_path}/{file_name}.json'

    with open(file_path_name_with_extension, 'r') as read_file:
        data = json.load(read_file)

    return data


def search_and_replace_in_file(path, search_for, replace_with):
    """
    Replace words in the file

    Args:
        path (str): path
        search_for (str): search string. Use ',' for more than once
        replace_with (str): replace string. Use ',' for more than once

    Returns:
        str: path
    """

    search_for = search_for.split(',')
    replace_with = replace_with.split(',')

    if len(search_for) != len(replace_with):
        cmds.error('Search for and replace with must have same number of words (split with commas)')

    with open(path, 'r+') as skin_file:
        lines = skin_file.readlines()
        skin_file.seek(0)
        skin_file.truncate()
        for line in lines:
            for index, value in enumerate(search_for):
                line = line.replace(value, replace_with[index])
            skin_file.writelines(line)

    return path
