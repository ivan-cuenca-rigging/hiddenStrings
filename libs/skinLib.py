# Imports
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import sideLib, usageLib, jsonLib


def set_labels():
    joint_list = cmds.ls(type='joint')

    for jnt in joint_list:
        if len(jnt.split('_')) == 3:
            desc, side, usage = jnt.split('_')
            usage_capitalize = '{}{}'.format(usage[0].upper(), usage[1:])

            if side == sideLib.center:
                cmds.setAttr('{}.side'.format(jnt), 0)
            if side == sideLib.left:
                cmds.setAttr('{}.side'.format(jnt), 1)
            if side == sideLib.right:
                cmds.setAttr('{}.side'.format(jnt), 2)

            cmds.setAttr('{}.type'.format(jnt), 18)
            cmds.setAttr('{}.otherType'.format(jnt), '{}{}'.format(desc, usage_capitalize), type='string')

            print(end='labels has been set')
        else:
            cmds.setAttr('{}.type'.format(jnt), 18)
            cmds.setAttr('{}.otherType'.format(jnt), jnt, type='string')
            cmds.warning('{} has an incorrect name, should be renamed with the following pattern:'
                         ' descriptor_side_usage'.format(jnt))


def set_skin_pose(*args):
    """
    Set all controls in the scene to default and then apply the skin pose attribute if exists, the skin pose is in
    objectSpace and does not take into account follows settings
    """
    skin_pose_attr = 'skinPoseData'

    control_list = cmds.ls('*_{}'.format(usageLib.control))

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
    Format the skin_cluster_name
    :param node: str
    :param skin_index: int
    :return: skinCluster name
    """
    if len(node.split('_')) != 3:
        return '{}{}_{}'.format(node, str(skin_index).zfill(2), usageLib.skin_cluster)
    else:
        descriptor, side, usage = node.split('_')
        return '{}{}{}_{}_{}'.format(descriptor, usage.capitalize(), str(skin_index).zfill(2),
                                     side,
                                     usageLib.skin_cluster)


def rename_skin_cluster(skin_cluster):
    """
    Rename skinCluster name
    :param skin_cluster: str
    :return: skinCluster name
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
                        skin_index=1):
    """
    create skinCluster by default
    :param joints: list
    :param node: str, geometry, nurbs, curve, etc
    :param skin_index: int
    :return: skinCluster
    """
    if skin_index == 1:
        skin_cluster = cmds.skinCluster(joints, node,
                                        toSelectedBones=True,
                                        bindMethod=0,
                                        removeUnusedInfluence=False,
                                        includeHiddenSelections=True,
                                        obeyMaxInfluences=False)[0]
    else:
        last_skin = skin_index - 1
        last_skin_name = format_skin_cluster_name(node, last_skin)
        if not cmds.objExists(last_skin_name):
            cmds.error('{} does not exists, cannot create a {} skin index skinCluster'.format(last_skin_name,
                                                                                              skin_index))
        node_dup = cmds.duplicate(node)[0]
        skin_cluster = cmds.skinCluster(joints, node_dup,
                                        toSelectedBones=True,
                                        bindMethod=0,
                                        removeUnusedInfluence=False,
                                        includeHiddenSelections=True,
                                        obeyMaxInfluences=False)[0]

        # Connect new skin between last skin and last skin connection
        skin_connection = cmds.listConnections('{}.outputGeometry'.format(last_skin_name), plugs=True)[0]

        cmds.connectAttr('{}.originalGeometry'.format(last_skin_name),
                         '{}.originalGeometry'.format(skin_cluster), force=True)
        cmds.connectAttr('{}.outputGeometry[0]'.format(last_skin_name),
                         '{}.input[0].inputGeometry'.format(skin_cluster), force=True)

        cmds.connectAttr('{}.outputGeometry[0]'.format(skin_cluster), skin_connection, force=True)

        cmds.delete(node_dup)

    skin_cluster = cmds.rename(skin_cluster, format_skin_cluster_name(node, skin_index))

    return skin_cluster


def get_skin_cluster_list(node):
    """
    Find skinClusters attached to the node
    :param node: str
    :return: skinCluster list
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
    :param node: str
    :param index: int. -1 (last), 1, 2, 3
    :return: skinCluster
    """
    if index >= 1:
        index = index-1
    if len(get_skin_cluster_list(node)) - 1 >= index:
        return get_skin_cluster_list(node)[index]
    else:
        return None


def transfer_skin(source, target, source_skin_index=1, target_skin_index=1, surface_association='closestComponent'):
    """
    Transfer skin from one object to another
    :param source: str
    :param target: str
    :param source_skin_index: int. -1 (last), 1, 2, 3
    :param target_skin_index: int. -1 (last), 1, 2, 3
    :param surface_association: closestPoint or closestComponent
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
        rename_skin_cluster(target_skin_cluster)

    # If skinCluster does not exist create it
    else:
        target_skin_cluster = create_skin_cluster(joints=source_skin_joints, node=target, skin_index=target_skin_index)

    # Transfer skinCluster
    set_labels()
    cmds.copySkinWeights(sourceSkin=source_skin_cluster, destinationSkin=target_skin_cluster,
                         surfaceAssociation=surface_association,
                         influenceAssociation='label')


def export_skin_cluster(node, path, skin_index=1):
    """
    Export skinCluster index of the node given if index == None then all index will be exported
    :param node: str
    :param path: str
    :param skin_index: int. -1 (last), 1, 2, 3
    """
    if skin_index:
        skin_cluster = rename_skin_cluster(get_skin_cluster_index(node, skin_index))
        skin_path = r'{}\{}.json'.format(path, skin_cluster)
        # Check if the file exists and is writable
        if os.path.exists(skin_path) and not os.access(skin_path, os.W_OK):
            cmds.warning('{} is not writeable. Check Permissions'.format(skin_path))
        else:
            # Export JSON
            cmds.deformerWeights('{}.json'.format(skin_cluster), deformer=skin_cluster, method='index',
                                 export=True, format='JSON', path=path)
    else:
        skin_cluster_list = get_skin_cluster_list(node)
        for skin_cluster in skin_cluster_list:
            skin_cluster = rename_skin_cluster(skin_cluster)
            skin_path = r'{}\{}.json'.format(path, skin_cluster)
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
    skin_cluster = get_skin_cluster_index(node, skin_index)
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
        rename_skin_cluster(skin_cluster)

    # If skinCluster does not exist create it
    else:
        skin_cluster = create_skin_cluster(joints=file_skin_joints, node=node, skin_index=skin_index)

    # Import skinCluster JSON
    cmds.deformerWeights(file_name, path=path, deformer=skin_cluster,
                         im=True, edit=True, method=import_method)

    print(end='\n')
    print(end='{} has been imported'.format(file_name))


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

        import_skin_cluster(node=node, path=r'{}\{}'.format(path, skin_file),
                            skin_index=skin_index, import_method=import_method)
