# Imports
import logging

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import side_lib, usage_lib

logging = logging.getLogger(__name__)


def set_labels():
    """
    Set the joints label for mirror and transfer skin tools
    """
    joint_list = cmds.ls(type='joint')

    for jnt in joint_list:
        if len(jnt.split('_')) == 3:
            desc, side, usage = jnt.split('_')
            usage_capitalize = '{}{}'.format(usage[0].upper(), usage[1:])

            if side == side_lib.center:
                cmds.setAttr('{}.side'.format(jnt), 0)
            if side == side_lib.left:
                cmds.setAttr('{}.side'.format(jnt), 1)
            if side == side_lib.right:
                cmds.setAttr('{}.side'.format(jnt), 2)

            cmds.setAttr('{}.type'.format(jnt), 18)
            cmds.setAttr('{}.otherType'.format(jnt), '{}{}'.format(desc, usage_capitalize), type='string')

            logging.info('labels has been set.')
        else:
            cmds.setAttr('{}.type'.format(jnt), 18)
            cmds.setAttr('{}.otherType'.format(jnt), jnt, type='string')
            logging.info('{} has an incorrect name, should be renamed with the following pattern:'
                         ' descriptor_side_usage.'.format(jnt))


def set_skin_pose(*args):
    """
    Set all controls in the scene to default and then apply the skin pose attribute if exists, the skin pose is in
    objectSpace and does not take into account follows settings
    """
    skin_pose_attr = 'skinPoseData'

    control_list = cmds.ls('*_{}'.format(usage_lib.control))

    for ctr in control_list:
        user_attrs = cmds.listAttr(ctr, userDefined=True)
        if user_attrs:
            for user_attr in cmds.listAttr(ctr, userDefined=True):
                try:
                    user_attr_dv = cmds.attributeQuery(user_attr, node=ctr, listDefault=True)[0]
                    cmds.setAttr('{}.{}'.format(ctr, user_attr), user_attr_dv)
                except:
                    pass

        for attr in 'trs':
            for axis in 'xyz':
                attr_value = 1 if attr == 's' else 0
                try:
                    cmds.setAttr('{}.{}{}'.format(ctr, attr, axis), attr_value)
                except:
                    pass

        if cmds.attributeQuery(skin_pose_attr, node=ctr, exists=True):
            skin_pose_data = cmds.getAttr('{}.{}'.format(ctr, skin_pose_attr))
            skin_pose_data = skin_pose_data.split('[')[-1].split(']')[0].split(',')
            skin_pose_data = [float(x) for x in skin_pose_data]

            cmds.xform(ctr, objectSpace=True, matrix=skin_pose_data)


def format_skin_cluster_name(node,
                             skin_index=1):
    """
    Format the skinCluster name

    Args:
        node (str): node's name
        skin_index (int): number of the skin to format
    
    Returns:
        str: skinCluster name
    """
    if len(node.split('_')) != 3:
        return '{}{}_{}'.format(node, str(skin_index).zfill(1), usage_lib.skin_cluster)
    else:
        descriptor, side, usage = node.split('_')
        return '{}{}{}_{}_{}'.format(descriptor, usage.capitalize(), str(skin_index).zfill(1),
                                     side,
                                     usage_lib.skin_cluster)


def rename_skin_cluster(skin_cluster):
    """
    Rename skinCluster name
    
    Args:
        skin_cluster (str): skin cluster to rename
    
    Returns:
        str: skinCluster name
    """
    node_shape = cmds.skinCluster(skin_cluster, query=True, geometry=True)[0]
    node = cmds.listRelatives(node_shape, parent=True)[0]

    skin_cluster_list = get_skin_cluster_list(node)
    skin_index = skin_cluster_list.index(skin_cluster) + 1

    skin_cluster = cmds.rename(skin_cluster, format_skin_cluster_name(node, skin_index))

    return skin_cluster


def rename_all_skin_clusters():
    """
    Rename all the skinClusters in the scene
    """
    skin_cluster_list = cmds.ls(type='skinCluster')
    for skin_cluster in skin_cluster_list:
        rename_skin_cluster(skin_cluster)


def create_skin_cluster(node,
                        joints,
                        prebinds=None,
                        skin_index=1):
    """
    Create skinCluster by default

    Args:
        node (str):, geometry, nurbs, curve, etc
        joints (list): list of joints to bind
        prebinds (list): list of prebinds. Defaults to None.
        skin_index (int): index of the skin. Defaults to 1.
    
    Returns:
        str: skinCluster
    """
    deformer_list = cmds.listHistory(node, pruneDagObjects=True)

    if prebinds:
        for prebind in prebinds:
            if not cmds.objExists(prebind):
                logging.error('{} does not exists in the scene'.format(prebind))

    if deformer_list:
        node_shape = cmds.listRelatives(node, shapes=True, noIntermediate=True)[0]

        output_geometry_connection = [x for x in cmds.listConnections(
            '{}'.format(node_shape), plugs=True) if 'outputGeometry' in x][0]


        node_connection = cmds.listConnections(output_geometry_connection, plugs=True)[0]
        last_deformer = output_geometry_connection.split('.')[0]

        connection_index = output_geometry_connection.split('[')[-1].split(']')[0]
        original_geometry_connection = cmds.listConnections('{}.originalGeometry[{}]'.format(last_deformer,
                                                                                             connection_index),
                                                                                             plugs=True)[0]

        node_dup = cmds.duplicate(node)[0]

        skin_cluster = cmds.skinCluster(joints,
                                        node_dup,
                                        toSelectedBones=True,
                                        bindMethod=0,
                                        removeUnusedInfluence=False,
                                        includeHiddenSelections=True,
                                        obeyMaxInfluences=False)[0]

        # Connect new skin between last deform and node
        cmds.connectAttr(original_geometry_connection,
                            '{}.originalGeometry[0]'.format(skin_cluster), force=True)
        cmds.connectAttr(output_geometry_connection,
                            '{}.input[0].inputGeometry'.format(skin_cluster), force=True)

        cmds.connectAttr('{}.outputGeometry[0]'.format(skin_cluster), node_connection, force=True)

        cmds.delete(node_dup)

    else:
        skin_cluster = cmds.skinCluster(joints, 
                                        node,
                                        toSelectedBones=True,
                                        bindMethod=0,
                                        removeUnusedInfluence=False,
                                        includeHiddenSelections=True,
                                        obeyMaxInfluences=False)[0]
        
    # Rename skinCluster
    skin_cluster = cmds.rename(skin_cluster, format_skin_cluster_name(node, skin_index))
    
    if prebinds:
        for index, prebind in enumerate(prebinds):
            if prebind:
                if '.' in prebind:
                        descriptor, side = joints[index].split('_')[:2]
                        inverse_matrix = cmds.createNode(
                            'inverseMatrix',
                            name='{}{}_{}_{}'.format(descriptor,
                                                     usage_lib.get_usage_capitalize(usage_lib.prebind),
                                                     side, usage_lib.inverse_matrix))
                        cmds.connectAttr(prebind, '{}.inputMatrix'.format(inverse_matrix))
                        cmds.connectAttr('{}.outputMatrix'.format(inverse_matrix),
                                        '{}.bindPreMatrix[{}]'.format(skin_cluster, index))
                else:
                    cmds.connectAttr('{}.worldInverseMatrix'.format(prebind),
                                    '{}.bindPreMatrix[{}]'.format(skin_cluster, index))

    return skin_cluster


def get_skin_cluster_list(node):
    """
    Find skinClusters attached to the node

    Args:
        node (str): node's name
    
    Returns:
        list: skinClusters list
    """
    skin_cluster_list = list()
    inputs_list = cmds.listHistory(node, interestLevel=1, pruneDagObjects=True)
    if inputs_list:
        for item in inputs_list:
            if cmds.objectType(item) == 'skinCluster':
                skin_cluster_list.append(item)
        skin_cluster_list = skin_cluster_list[::-1]

    return skin_cluster_list


def get_skin_cluster_index(node, index=1):
    """
    Find the skinCluster index

    Args:
        node (str): node's name
        index (int):. -1 (last), 1, 2, 3. Defaults to 1.
    
    Returns:
        str: skinCluster
    """
    if index >= 1:
        index = index - 1
    if len(get_skin_cluster_list(node)) - 1 >= index:
        return get_skin_cluster_list(node)[index]
    else:
        return None


def transfer_skin(source, target, source_skin_index=1, target_skin_index=1, surface_association='closestComponent'):
    """
    Transfer skin from one object to another

    Args:
        source (str): source node
        target (str): target node
        source_skin_index (int):. -1 (last), 1, 2, 3. Defaults to 1.
        target_skin_index (int):. -1 (last), 1, 2, 3. Defaults to 1.
        surface_association (str): closestPoint or closestComponent. Defaults to 'closestComponent'.
    """
    source_skin_cluster = get_skin_cluster_index(node=source, index=source_skin_index)
    if not source_skin_cluster:
        cmds.error('{} skinCluster index {} does not exists'.format(source, source_skin_index))
    source_skin_joints = cmds.skinCluster(source_skin_cluster, query=True, influence=True)

    target_skin_cluster = get_skin_cluster_index(node=target, index=target_skin_index)

    # If skinCluster exists get its joints and add the joints that are not in the skinCluster
    if target_skin_cluster:
        skin_cluster_joints = cmds.skinCluster(target_skin_cluster, query=True, influence=True)
        joints_to_add = [x for x in source_skin_joints if x not in skin_cluster_joints]

        cmds.skinCluster(target_skin_cluster, edit=True, addInfluence=joints_to_add, lockWeights=True)

    # If skinCluster does not exist create it
    else:
        target_skin_cluster = create_skin_cluster(joints=source_skin_joints, node=target, skin_index=target_skin_index)

    # Transfer skinCluster
    set_labels()
    cmds.copySkinWeights(sourceSkin=source_skin_cluster, destinationSkin=target_skin_cluster,
                         surfaceAssociation=surface_association,
                         noMirror=True,
                         influenceAssociation='label',
                         normalize=True)


def add_joint_to_skin_cluster(joint_name, skin_cluster_name, prebind_name=None):
    """
    Add a joint to an existing skinCluster

    Args:
        prebind_name (str):name of the prebind node or node.attribute
        joint_name (str): name of the joint to include
        skin_cluster_name (str): name of the skinCluster
    """
    # Checks
    if not cmds.objExists(joint_name):
        logging.error('{} does not exists in the scene'.format(joint_name))
    if not cmds.objExists(skin_cluster_name):
        logging.error('{} does not exists in the scene'.format(skin_cluster_name))
    if prebind_name:
        if not cmds.objExists(prebind_name):
            logging.error('{} does not exists in the scene'.format(prebind_name))

    # Create a tmp skin to create some attributes in the joint
    cube_temp = cmds.polyCube()[0]
    cmds.skinCluster(joint_name,
                     cube_temp,
                     toSelectedBones=True,
                     bindMethod=0,
                     removeUnusedInfluence=False,
                     includeHiddenSelections=True,
                     obeyMaxInfluences=False)[0]
    cmds.delete(cube_temp)
    
    # Get next joint skin index for the skinCluster connections
    joint_index = str(len(cmds.listConnections('{}.matrix'.format(skin_cluster_name))))

    # Create connections
    cmds.connectAttr('{}.worldMatrix[0]'.format(joint_name),
                     '{}.matrix[{}]'.format(skin_cluster_name, joint_index))
    cmds.connectAttr('{}.lockInfluenceWeights'.format(joint_name),
                     '{}.lockWeights[{}]'.format(skin_cluster_name, joint_index))
    cmds.connectAttr('{}.objectColorRGB'.format(joint_name),
                     '{}.influenceColor[{}]'.format(skin_cluster_name, joint_index))

    # If prebind exists then connect it, else set to its default value
    if prebind_name:
        if '.' in prebind_name:
            descriptor, side = joint_name.split('_')[:2]
            inverse_matrix = cmds.createNode(
                'inverseMatrix', 
                name='{}{}_{}_{}'.format(descriptor, usage_lib.get_usage_capitalize(usage_lib.prebind),
                                         side, usage_lib.inverse_matrix))
            cmds.connectAttr(prebind_name, '{}.inputMatrix'.format(inverse_matrix))
            cmds.connectAttr('{}.outputMatrix'.format(inverse_matrix), 
                             '{}.bindPreMatrix[{}]'.format(skin_cluster_name, joint_index))
        else:
            cmds.connectAttr('{}.worldInverseMatrix'.format(prebind_name),
                            '{}.bindPreMatrix[{}]'.format(skin_cluster_name, joint_index))
    else:
        cmds.setAttr('{}.bindPreMatrix[{}]'.format(skin_cluster_name, joint_index),
                     cmds.getAttr('{}.worldInverseMatrix'.format(joint_name)),
                     type='matrix')
